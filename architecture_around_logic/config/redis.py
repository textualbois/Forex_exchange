from dotenv import dotenv_values


config = dotenv_values(".env")

REDIS_host = config["REDIS_host"]
REDIS_port = int(config["REDIS_port"])
REDIS_db = int(config["REDIS_db"])
REDIS_QUEUE = int(config["REDIS_queue_db"])