from rq import Worker
from architecture_around_logic.src.connections import r_queue_connection

worker = Worker(["Live interactions", "Requests"], connection=r_queue_connection)
worker.work()
