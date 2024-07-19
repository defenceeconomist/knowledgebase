from shiny import Inputs, Outputs, Session, module, ui, reactive
from ragmodule.about import about_ui
from ragmodule.rag_chain import rag_chain

@module.server
def rag_server(input: Inputs, output: Outputs, session: Session, vectordb, llm, redis_cons):
  
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
    
    # Run query when ask button is clicked
    @reactive.effect
    @reactive.event(input.ask, ignore_init=True, ignore_none=True)
    def _():
        query = input.query()
        print(rag_chain(
            query = query, 
            vectordb = vectordb, 
            llm = llm, 
            redis_cons = redis_cons
            ))
