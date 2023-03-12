import redis
from rq import Worker
from architecture_around_logic.config.redis import REDIS_port, REDIS_QUEUE, REDIS_host


print(f'Redis host is {REDIS_host}\n'
      f'redis port is {REDIS_port}\n'
      f'redis QUEUE code is {REDIS_QUEUE}\n')

r_queue = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_QUEUE)

worker = Worker(["Live interactions", "Requests"], connection=r_queue)
worker.work()
