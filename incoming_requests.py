import time
import redis
from rq import Queue, Worker, job
from dotenv import dotenv_values
import telebot
from telebot import types
import sqlite3
import contacts
import main_db
import redis_db as rf
import bot_markups as btmrkp
import re
import message_maker as mm

import pickle

config = dotenv_values(".env")
print("\n\n\n\n\n")
API_KEY = config["API_KEY"]
REDIS_host = config["REDIS_host"]
REDIS_port = int(config["REDIS_port"])
REDIS_DB = int(config["REDIS_db"])
REDIS_QUEUE = int(config["REDIS_queue_db"])
print(f'Redis host is {REDIS_host}\n'
      f'redis port is {REDIS_port}\n'
      f'redis db is {REDIS_DB}\n')


bot = telebot.TeleBot(API_KEY)
r = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_DB, decode_responses=True)
r_queue = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_QUEUE)

Q_hi = Queue("Live interactions", connection=r_queue)
Q_lo = Queue("Requests", connection=r_queue)


def test_for_contacts(user_id, db_file):
	contacts_complete_job = Q_hi.enqueue(contacts.contacts_is_complete, user_id, db_file)
	Q_hi.enqueue(show_bids_or_ask_for_contacts, user_id, db_file, contacts_complete_job.id,
				 depends_on=contacts_complete_job)


def show_bids_or_ask_for_contacts(user_id, db_file, contacts_complete_job_id):
	has_contacts = job.Job.fetch(contacts_complete_job_id).result
	if has_contacts:
		Q_hi.enqueue(show_bids, user_id, db_file)
	else:
		Q_hi.enqueue(ask_for_contacts, user_id)


def ask_for_contacts(user_id):
	msg = ("Чтобы просмотреть входящие заявки необходимо заполнить свои контактные данные. "
		   "Это можно сделать в основном меню под вкладкой 'Мои Данные'.")
	bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_menu_start(user_id))


def show_bids(user_id, db_file):
	bids_with_incoming_requests = main_db.bids_with_incoming_requests_full_row(user_id, db_file)
	assert isinstance(bids_with_incoming_requests, list), "bids_with_incoming_requests should be a list.\n"
	if len(bids_with_incoming_requests) == 0:
		send_you_have_no_incoming_requests(user_id)
	else:
		bid_data = main_db.get_bid_data_by_bid_id()





def send_you_have_no_incoming_requests(user_id):
	msg = "У вас пока нет запросов на обмен"
	bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_menu_start(user_id))
