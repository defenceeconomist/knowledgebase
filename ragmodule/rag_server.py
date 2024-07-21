from shiny import Inputs, Outputs, Session, module, ui, reactive, render
from ragmodule.about import about_ui
from ragmodule.rag_chain import rag_chain
from langchain_community.chat_message_histories import RedisChatMessageHistory

@module.server
def rag_server(input: Inputs, output: Outputs, session: Session, vectordb, llm, redis_cons, token):
    chat_history = reactive.Value()
    @reactive.effect
    def _():
        chat_history.set(RedisChatMessageHistory(
            token.get(), url=redis_cons["redis_url"]
        ))
    
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
        chat_history.set(rag_chain(
            query = query, 
            vectordb = vectordb, 
            llm = llm, 
            redis_cons = redis_cons, 
            session_id = token.get()
            ))
    
    # Show the chat history as markdown (ui.response)
    @render.ui
    def response():
        html_out = []
        for msg in chat_history().messages:
            html_out.append(f"<p><b>{msg.type}:</b> {msg.content}</p>")
        return ui.HTML("".join(html_out))
        
