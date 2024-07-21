from kbutils.load_config import load_config
from kbutils.langchain_chroma import connect_vectordb
from kbutils.langchain_openai import langchain_openai
from kbutils.connect_redis import get_redis_connections

from shiny import Inputs, Outputs, Session, App, ui, reactive, render
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
    ui.head_content(ui.include_js(Path(__file__).parent / "www" / "cookies" / "js.cookie.min.js")),
    # RAG Module UI
    ui.nav_panel(
        "Retrieval Augmented Generation",
        rag_ui("rag"),
        ui.input_text("name_set", "What is your name?"),
        ui.input_action_button("save", "Save Cookie"),
        ui.input_action_button("remove", "Remove Cookie"),
        ui.output_ui("name_get")

    ),
    ui.nav_spacer(),
    ui.nav_control(ui.tags.a("The Defence Economist")),
    title = "Knowledge Base",
    fillable = True
    )
      
def server(input: Inputs, output: Outputs, session: Session):
    rag_server("rag", vectordb=vectordb, llm=llm, redis_cons = redis_cons)

    @render.ui
    def name_get():
        if input.cookies()["name"] is None:
            out = ui.h3("What is your name?")
        else:
            out = ui.h3("Hello ", input.cookies()["name"])
        return out
    
    @reactive.effect
    @reactive.event(input.save)
    async def _():
        msg = {"name": "name", "value": input.name_set()}
        await session.send_custom_message("cookie-set", msg)

app_dir = Path(__file__).parent
app = App(app_ui, server,  static_assets=app_dir / "www")
