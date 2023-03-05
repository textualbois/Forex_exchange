import os

import redis
from rq import Queue, Worker
from dotenv import dotenv_values
import sqlite3
import redis_db as rf
import bot_markups as btmrkp
import telebot
# noinspection PyUnresolvedReferences
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

config = dotenv_values(".env")
print("\n\n\n\n\n")
API_KEY = config["API_KEY"]
REDIS_host = config["REDIS_host"]
REDIS_port = int(config["REDIS_port"])
REDIS_DB = int(config["REDIS_db"])
REDIS_QUEUE = int(config["REDIS_queue_db"])
print(f'Redis host is {REDIS_host}\n'
      f'redis port is {REDIS_port}\n'
      f'redis db code is {REDIS_DB}\n'
      f'redis QUEUE code is {REDIS_QUEUE}\n')


bot = telebot.TeleBot(API_KEY)
r = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_DB, decode_responses=True)
r_queue = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_QUEUE)

worker = Worker(["Live interactions", "Requests"], connection=r_queue)
worker.work()
