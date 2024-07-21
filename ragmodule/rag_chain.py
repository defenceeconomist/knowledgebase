from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.globals import set_llm_cache

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.cache import RedisCache

def rag_chain(query, vectordb, llm, redis_cons):
  
  set_llm_cache(RedisCache(redis_cons["redis_client"]))
  retriever = vectordb.as_retriever()
  
  contextualize_q_system_prompt = (
      "Given a chat history and the latest user question "
      "which might reference context in the chat history, "
      "formulate a standalone question which can be understood "
      "without the chat history. Do NOT answer the question, "
      "just reformulate it if needed and otherwise return it as is."
  )

  contextualize_q_prompt = ChatPromptTemplate.from_messages(
      [
          ("system", contextualize_q_system_prompt),
          MessagesPlaceholder("chat_history"),
          ("human", "{input}"),
      ]
  )

  history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
    )
  
  system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
    )

  qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )

  question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
  rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain) 

  conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    lambda session_id: RedisChatMessageHistory(
        session_id, url=redis_cons["redis_url"]
    ),
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
    )
  
  return(conversational_rag_chain.invoke(
    {"input": query},
    config={
        "configurable": {"session_id": "abc123"} # TODO Generate a session id based on user cookie
    },  # constructs a key "abc123" in `store`.
    )["answer"])
