from shiny import  ui

def about_ui():
  # ' generate the about UI
   with open('./ragmodule/about.md', "r") as f:
    about_md = " ".join(f.readlines())
    
    return ui.TagList(
         ui.markdown(about_md)
        )
        