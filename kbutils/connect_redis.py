import redis

def connect_redis(config):
    return(redis.Redis(
        host=config["REDIS"][0]["host"],
        port=config["REDIS"][0]["port"],
        password=config["REDIS_API_KEY"]
        ))

def generate_redis_url(config):
    
    host=config["REDIS"][0]["host"]
    port = config["REDIS"][0]["port"]
    redis_api_key = config["REDIS_API_KEY"]

    return(f"redis://default:{redis_api_key}@{host}:{port}")

def get_redis_connections(config):
    return({
        "redis_client": connect_redis(config = config), 
        "redis_url": generate_redis_url(config)
     })

