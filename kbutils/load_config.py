import os
from dotenv import load_dotenv
import yaml
import re

load_dotenv()

def load_config(
        config_yaml_path = "config.yaml", 
        openai_api_key = os.getenv("OPENAI_API_KEY"),
        redis_api_key = os.getenv("REDIS_API_KEY")
        ):
    with open(config_yaml_path, "r") as f:
        config = yaml.safe_load(f)

    config["OPENAI_API_KEY"] = openai_api_key  
    config["REDIS_API_KEY"] = redis_api_key
    
    return(config)

