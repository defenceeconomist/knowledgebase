from shiny import module, render, ui, Inputs, Outputs, Session
@module.ui
def row_ui():
    return ui.row(
        ui.column(6, ui.input_text("text_in", "Enter text")),
        ui.column(6, ui.output_text("text_out")),
    )


@module.server
def row_server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def text_out():
        return f"You entered {input.text_in()}"
