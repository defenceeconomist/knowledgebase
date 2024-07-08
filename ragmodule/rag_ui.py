from shiny import  ui, module
from kbutils.icons import paper_plane

@module.ui
def rag_ui():
    page_sidebar = ui.sidebar(
            ui.h4("About"),
            ui.tags.span(
                "This application uses ",
                ui.input_action_link(
                    id = "info",
                    label = "Retrieval Augmented Generation"
                ),
                " to query an expanding knowledge base ",
                "about Defence, Economics and Evaluation.",
                style = "display: block-inline",
                class_ = "help-block"
                )
            )

        
    page_main = ui.TagList(
        ui.card(
            ui.output_ui("response"),
            fill=True
            ), 
        ui.card(
            ui.row(
                ui.column(
                    11,
                        ui.input_text_area(
                        "query", 
                        None, 
                        "What would you like to know about?", 
                        width="100%",
                        autoresize=True,
                        resize="vertical"
                    ) 
                ),
                ui.column(
                    1,
                    ui.input_action_button(
                        id ="ask", 
                        label = None, 
                        icon = paper_plane,
                        width = "100%"),
                )
            ),
            fill=False  
            ),
        ui.help_text("Chat GPT can make mistakes. Consider checking important information.",
                        style = "text-align: center")
    )

    return(ui.layout_sidebar(
        page_sidebar,
        page_main
        ))