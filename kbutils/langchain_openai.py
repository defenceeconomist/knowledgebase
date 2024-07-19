from langchain_openai import ChatOpenAI
def langchain_openai(config):
    return(ChatOpenAI(model=config["DEFAULT_MODEL"],api_key=config["OPENAI_API_KEY"]))