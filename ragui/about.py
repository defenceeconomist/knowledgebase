from shiny import App, Inputs, Outputs, Session, module, render, ui, reactive


def about_ui():
  # ' generate the about UI
   with open('./ragui/about.md', "r") as f:
    about_md = " ".join(f.readlines())
    
    return ui.TagList(
         ui.markdown(about_md)
        )
        
