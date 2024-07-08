from shiny import Inputs, Outputs, Session, App, ui, module, reactive
from kbutils.helpers import load_config
from ragmodule.rag_server import rag_server
from ragmodule.rag_ui import rag_ui

config = load_config("config.yaml")

# Shiny Application
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
   rag_server("rag")

app = App(app_ui, server)

