from shiny import Inputs, Outputs, Session, App, ui, module, reactive
from ragmodule.icons import paper_plane
import yaml
from ragmodule.about import about_ui

# Load Config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

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

