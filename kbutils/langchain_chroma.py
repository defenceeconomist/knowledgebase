from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

def connect_vectordb():
    openai_ef = OpenAIEmbeddings(
        model="text-embedding-ada-002"
        )
    
    chromaclient = chromadb.PersistentClient(path="chromadb")

    return(Chroma(
        client=chromaclient,
        collection_name="defecon-kb",
        embedding_function=openai_ef,
    ))

