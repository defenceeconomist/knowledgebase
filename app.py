from shiny import App, Inputs, Outputs, Session, module, render, ui
from ragui.ui import rag_ui
from ragui.server import rag_server

import yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

app_ui = rag_ui("kb")

def server(input: Inputs, output: Outputs, session: Session):
   rag_server("kb", config)


app = App(app_ui, server)
