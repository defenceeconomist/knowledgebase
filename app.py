from kbutils.load_config import load_config
from kbutils.langchain_chroma import connect_vectordb
from kbutils.langchain_openai import langchain_openai
from kbutils.connect_redis import get_redis_connections

from shiny import Inputs, Outputs, Session, App, ui
from ragmodule.rag_ui import rag_ui
from ragmodule.rag_server import rag_server

# Load Config, LLM and Connect to Vector Database
config = load_config()
vectordb = connect_vectordb(config = config)
llm = langchain_openai(config = config)
redis_cons = get_redis_connections(config = config)

# Define App UI (ui components are modular)
app_ui = ui.page_navbar(   
    ui.nav_control(
        ui.tags.head(
            ui.include_css("./www/style.css")
            )),
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
   rag_server("rag", vectordb=vectordb, llm=llm, redis_cons = redis_cons)

app = App(app_ui, server)
