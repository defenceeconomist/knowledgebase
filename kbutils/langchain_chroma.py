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

vector_db = connect_vectordb()

# TODO 
# [x] Contextual compression
# [ ] Remembering previous question
# [ ] Citations
# [ ] Streaming
# [ ] Cache
 
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import OpenAI

def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )
retriever = vector_db.as_retriever()
query = 'What is realist evaluation?'
docs = retriever.invoke(query)
llm = OpenAI(temperature=0)
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

compressed_docs = compression_retriever.invoke(query)

pretty_print_docs(docs)
pretty_print_docs(compressed_docs)