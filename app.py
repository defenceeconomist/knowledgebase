from shiny import App, Inputs, Outputs, Session, module, render, ui
from ragui.ui import rag_ui
from ragui.server import rag_server

app_ui = rag_ui("knowledge_base")

def server(input: Inputs, output: Outputs, session: Session):
   rag_server("knowledge_base")


app = App(app_ui, server)
