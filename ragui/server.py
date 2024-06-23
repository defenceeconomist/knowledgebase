from shiny import App, Inputs, Outputs, Session, module, render, ui, reactive
from pathlib import Path

@module.server
def rag_server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.ui
    def about_ui():
       with open('./ragui/about.md', "r") as f:
        about_md = " ".join(f.readlines())
        
        return ui.TagList(
             ui.markdown(about_md),
             ui.output_image("image")
            )
        
    @reactive.Effect
    @reactive.event(input.info, ignore_init=True, ignore_none=True)
    def _():
        return ui.modal_show(
            ui.modal(
                ui.output_ui("about_ui"),
                size = "l"
            )
            )
    
    @output
    @render.image
    def image():     
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "../www/fig_1.png"), "width": "100%"}
        return img
