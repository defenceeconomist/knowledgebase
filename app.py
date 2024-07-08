from shiny import App, Inputs, Outputs, Session, module, render, ui
from ragui.ui import rag_ui
from ragui.server import rag_server

import yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

page_dependencies = ui.tags.head(ui.include_css("./www/style.css"))

app_ui = ui.page_navbar(   
    ui.nav_control(page_dependencies),
    ui.nav_panel(
        "Retrieval Augmented Generation",
        rag_ui("kb")
    ),
    ui.nav_spacer(),
    ui.nav_control(ui.tags.a("The Defence Economist")),
    title = "Knowledge Base",
    fillable = True
    )
      
   

def server(input: Inputs, output: Outputs, session: Session):
   rag_server("kb", config)


app = App(app_ui, server)
