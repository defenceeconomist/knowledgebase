from shiny import App, Inputs, Outputs, Session, module, render, ui, reactive
from pathlib import Path
from ragui.about import about_ui

@module.server
def rag_server(input: Inputs, output: Outputs, session: Session):
    
    chat_history_md: reactive.Value[str] = reactive.Value("Test")
    chat_string: reactive.Value[str] = reactive.Value("")
    
    # Show a modal when the about cog is clicked.
    @reactive.Effect
    @reactive.event(input.info, ignore_init=True, ignore_none=True)
    def _():
        return ui.modal_show(
            ui.modal(
                about_ui(),
                size = "l"
                )
            )
            
    # RAG -----
    @reactive.Effect
    @reactive.event(input.ask, ignore_init=True, ignore_none=True)
    def _():
      return ""
    
    
    
    @output
    @render.ui
    def response():
        return ui.TagList(
            ui.tags.script(
            "el = document.getElementById('kb-response').parentNode;" +
            "el.scrollTo(0, el.scrollHeight)"
            ), 
            ui.markdown(chat_history_md() + chat_string())
            )
            
    
