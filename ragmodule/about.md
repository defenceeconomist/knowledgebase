# Retrieval Augmented Generation

Retrieval augmented generation (RAG) is an AI technique that combines information retrieval with text generation, allowing AI models to retrieve relevant information from a knowledge source and incorporate it into generated text. 

RAG can improve the quality, accuracy, and relevance of the text output for various tasks, such as answering questions and summarising documents. RAG works by using an information retrieval system to find the most relevant documents or data for a given query or task. Then, it uses a large language model (LLM) to generate text based on the retrieved information and the query or task. RAG can also provide transparency and explainability for the generated text by showing the sources of information used by the model.

## How it works

1. Retrieve: The user query is used to retrieve relevant context from an external knowledge source. For this, the user query is embedded with an embedding model into the same vector space as the additional context in the vector database. This allows to perform a similarity search, and the top k closest data objects from the vector database are returned. In this implementation the OpenAI ada2 model is used for embeddings and chromadb used as a vector database. 
2. Augment: The user query and the retrieved additional context are stuffed into a prompt template.
3. Generate: Finally, the retrieval-augmented prompt is fed to the LLM. This implementation uses OpenAI ChatGPT 3.5.

Figure 1: Retrieval Augmented Generation Workflow

![](fig_1.png)