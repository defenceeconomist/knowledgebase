from kbutils.load_config import load_config
from kbutils.langchain_chroma import connect_vectordb
from kbutils.langchain_openai import langchain_openai
from kbutils.connect_redis import get_redis_connections

from shiny import Inputs, Outputs, Session, App, ui, reactive, render
import secrets
import bcrypt

from ragmodule.rag_ui import rag_ui
from ragmodule.rag_server import rag_server

from pathlib import Path

async def set_login_cookie(session, redis, user):
    # generate a selector, validator token and save as a cookie
    selector = secrets.token_urlsafe(6)
    validator = secrets.token_urlsafe(32)
    token = selector + ":" + validator
    await session.send_custom_message("cookie-set", {"name": "kb_token", "value": token})

    # upload selector and hashed validator to redis
    hashed_validator = bcrypt.hashpw(validator.encode("utf-8"), bcrypt.gensalt())
    redis.hset("tokens", mapping = {selector:hashed_validator})
    redis.hset("user_token", mapping = {selector:user})

# Load Config, LLM Client, Connect to Vector Database, Redis Connection Strings
config = load_config()
vectordb = connect_vectordb(config = config)
llm = langchain_openai(config = config)
redis_cons = get_redis_connections(config = config)

# Define App UI (ui components are modular)
app_ui = ui.page_fillable(
    # https://stackoverflow.com/questions/77047019/http-1-1-404-not-found-when-reading-external-js-and-css-file-in-shiny-python
    ui.head_content(ui.include_js(Path(__file__).parent / "www" / "shinyjs" / "script.js", defer = "")), 
    ui.head_content(ui.include_js(Path(__file__).parent / "www" / "cookies" / "js.cookie.min.js", defer = "")),
    ui.head_content(ui.include_css(Path(__file__).parent / "www" / "style.css")),
    ui.output_ui("content", fillable=True),
    gap = ui.css.as_css_unit(0),
    padding = ui.css.as_css_padding(0)
    )

def server(input: Inputs, output: Outputs, session: Session):

    user = reactive.value()
    logged_in = reactive.value(False)

    # Render main UI if logged in and display login panel if not logged in
    @render.ui
    def content():
        if logged_in():
            return(ui.page_navbar(
            ui.nav_panel(
            "Retrieval Augmented Generation",
                rag_ui("rag")
            ),
            ui.nav_spacer(),
            ui.nav_control(ui.tags.a("The Defence Economist")),
            title = "Knowledge Base",
            fillable = True))
        else:
            return(
                ui.column(4, 
                    ui.card(
                    ui.card_header("Knowledge Base"),
                    ui.input_text("username", "Enter Username"),
                     ui.input_password("password", "Enter Password"),
                    ui.card_footer(ui.input_action_button("login_button", "Login")),
                    full_screen=False,fill=False,
                    ),
                offset = 4
                )
            )
        
    # When login button is pressed check username and password against database
    # If login is successful change the logged_in reactive value
    # and set a token
    @reactive.effect
    @reactive.event(input.login_button)
    async def _():
        users = redis_cons["redis_client"].hgetall("users")
        if input.username().encode('utf-8') in users:
            stored_hash =  users[input.username().encode('utf-8')]
            if bcrypt.checkpw(input.password().encode('utf-8'), stored_hash):
                await set_login_cookie(session, redis_cons["redis_client"], input.username())  
            else:
                print("Incorrect password")
        else:
            print("Incorrect user")

    # Observe changes in kb_token cookie. If the token is validated then login.
    @reactive.effect
    def _():
        if "kb_token" in input.cookies():
            token = input.cookies()["kb_token"]
            selector = token.split(":")[0]
            validator = token.split(":")[1]
            tokens = redis_cons["redis_client"].hgetall("tokens")
            user_token = redis_cons["redis_client"].hgetall("user_token")
            hashed_validator = tokens[selector.encode("utf-8")]
            if bcrypt.checkpw(validator.encode("utf-8"), hashed_validator):
                logged_in.set(True)
                user.set(user_token[selector.encode("utf-8")].decode())
                print(f'Welcome {user_token[selector.encode("utf-8")].decode()}')

    # Load RAG Server Module    
    rag_server("rag", vectordb=vectordb, llm=llm, 
               redis_cons = redis_cons, 
               user = user)

app_dir = Path(__file__).parent
app = App(app_ui, server,  static_assets=app_dir / "www")
