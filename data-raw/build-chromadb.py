# Load the processed data 
import chromadb
import os
from dotenv import load_dotenv
load_dotenv()

from chromadb.utils import embedding_functions
client = chromadb.PersistentClient(path="chromadb")
client.list_collections()
#client.delete_collection("defecon-kb")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-ada-002"
            )

collection = client.create_collection(
    name = "defecon-kb",
    metadata={"hnsw:space": "cosine"},
    embedding_function=openai_ef
    )
