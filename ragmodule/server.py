from shiny import Inputs, Outputs, Session, module, ui, reactive
from ragmodule.about import about_ui

@module.server
def rag_server(input: Inputs, output: Outputs, session: Session):
  
    # Show a modal when the about link is clicked.
    @reactive.effect
    @reactive.event(input.info, ignore_init=True, ignore_none=True)
    def _():
        return ui.modal_show(
            ui.modal(
                about_ui(),
                size = "l"
                )
            )
