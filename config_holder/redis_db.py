import redis
from dotenv import dotenv_values

config = dotenv_values("../.env")
REDIS_host = config["REDIS_host"]
REDIS_port = int(config["REDIS_port"])
REDIS_DB = int(config["REDIS_db"])

r = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_DB, decode_responses=True)

