from shiny import App, Inputs, Outputs, Session, ui
import chromadb
from chromadb.utils import embedding_functions
from ragui.ui import rag_ui
from ragui.server import rag_server
import yaml
import os

# Load Config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load Chromadb
chromaclient = chromadb.PersistentClient(path="chromadb")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-ada-002"
                )

collection = chromaclient.get_collection(name="defecon-kb", embedding_function=openai_ef)

# Shiny Application
app_ui = ui.page_navbar(   
    ui.nav_control(
        ui.tags.head(
            ui.include_css("./www/style.css")
            )),
    # RAG Module UI
    ui.nav_panel(
        "Retrieval Augmented Generation",
        rag_ui("kb")
    ),
    ui.nav_spacer(),
    ui.nav_control(ui.tags.a("The Defence Economist")),
    title = "Knowledge Base",
    fillable = True
    )
      
def server(input: Inputs, output: Outputs, session: Session):
   # Load module server code
   rag_server("kb", config)

app = App(app_ui, server)
