# This script connects to redis and sets up a cache and history.

from langchain.globals import set_llm_cache
from langchain.cache import RedisCache
import redis
from dotenv import load_dotenv
import os
load_dotenv()
redis_api_Key = os.getenv("REDIS_API_KEY")
redis_url = f"redis://default:{redis_api_Key}@redis-19384.c293.eu-central-1-1.ec2.redns.redis-cloud.com:19384"

import redis

redis_client = redis.Redis(
  host='redis-19384.c293.eu-central-1-1.ec2.redns.redis-cloud.com',
  port=19384,
  password=redis_api_Key
  )


set_llm_cache(RedisCache(redis_client))

# https://js.langchain.com/v0.1/docs/integrations/chat_memory/redis/

from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import RedisChatMessageHistory
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatOpenAI()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: RedisChatMessageHistory(
        session_id, url=redis_url
    ),
    input_messages_key="question",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "foo"}}

chain_with_history.invoke({"question": "Hi! I'm bob"}, config=config)

chain_with_history.invoke({"question": "Whats my name"}, config=config)
