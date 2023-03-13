import redis
from architecture_around_logic.config.redis import REDIS_port, REDIS_QUEUE, REDIS_host


r_queue_connection = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_QUEUE)
