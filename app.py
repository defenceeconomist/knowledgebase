from shiny import App, Inputs, Outputs, Session, module, render, ui
from ragui.core import row_ui, row_server



extra_ids = ["row_3", "row_4", "row_5"]

app_ui = ui.page_fluid(
    row_ui("row_1"),
    row_ui("row_2"),    
    [row_ui(x) for x in extra_ids]
)


def server(input: Inputs, output: Outputs, session: Session):
    row_server("row_1")
    row_server("row_2")
    [row_server(x) for x in extra_ids]


app = App(app_ui, server)