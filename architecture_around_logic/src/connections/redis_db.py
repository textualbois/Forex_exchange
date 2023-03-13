import redis
from architecture_around_logic.config.redis import REDIS_port, REDIS_db, REDIS_host

r = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_DB, decode_responses=True)
