from kbutils.load_config import load_config
from kbutils.langchain_chroma import connect_vectordb
from kbutils.langchain_openai import langchain_openai
from kbutils.connect_redis import get_redis_connections

from shiny import Inputs, Outputs, Session, App, ui, reactive, render
import secrets

from ragmodule.rag_ui import rag_ui
from ragmodule.rag_server import rag_server

from pathlib import Path

# Load Config, LLM Client, Connect to Vector Database, Redis Connection Strings
config = load_config()
vectordb = connect_vectordb(config = config)
llm = langchain_openai(config = config)
redis_cons = get_redis_connections(config = config)

# Define App UI (ui components are modular)
app_ui = ui.page_navbar(
    # https://stackoverflow.com/questions/77047019/http-1-1-404-not-found-when-reading-external-js-and-css-file-in-shiny-python
    ui.head_content(ui.include_js(Path(__file__).parent / "www" / "shinyjs" / "script.js", defer = "")), 
    ui.head_content(ui.include_js(Path(__file__).parent / "www" / "cookies" / "js.cookie.min.js", defer = "")),
    ui.head_content(ui.include_css(Path(__file__).parent / "www" / "style.css")),
    # RAG Module UI
    ui.nav_panel(
        "Retrieval Augmented Generation",
        rag_ui("rag")
    ),
    ui.nav_spacer(),
    ui.nav_control(ui.tags.a("The Defence Economist")),
    title = "Knowledge Base",
    fillable = True
    )
      
def server(input: Inputs, output: Outputs, session: Session):
    vals = reactive.value()

    @reactive.effect
    async def _():
        if not "kb_token" in input.cookies():
            msg = {"name": "kb_token", "value": secrets.token_urlsafe(16)}
            await session.send_custom_message("cookie-set", msg)       
        else:
            vals.set(input.cookies()['kb_token'])
            
    rag_server("rag", vectordb=vectordb, llm=llm, 
               redis_cons = redis_cons, 
               token = vals)

app_dir = Path(__file__).parent
app = App(app_ui, server,  static_assets=app_dir / "www")
