 # todo ограничить количество запрос на одну заявку (1 запрос на 1 заявку)
 # todo добавить функционал заявок с множественными запросами

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
import dict_management
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
		Q_hi.enqueue(rf.reset_shown_data_count, user_id)
		Q_hi.enqueue(show_bids, user_id, db_file)
	else:
		Q_hi.enqueue(ask_for_contacts, user_id)


def ask_for_contacts(user_id):
	msg = ("Чтобы просмотреть входящие заявки необходимо заполнить свои контактные данные. "
		   "Это можно сделать в основном меню под вкладкой 'Мои Данные'.")
	bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_menu_start(user_id))


 # Todo refactor else: part and add main_db function to take list of bid_id's and
 # Todo not loop overbids_with_incoming_requests or there will be too much conn's to the db
def show_bids(user_id, db_file):
	bids_with_incoming_requests = main_db.bids_with_incoming_requests_full_row(user_id, db_file)
	assert isinstance(bids_with_incoming_requests, list), "bids_with_incoming_requests should be a list.\n"
	if len(bids_with_incoming_requests) == 0:
		send_you_have_no_incoming_requests(user_id)
	else:
		bid_data = []
		for incoming_request in bids_with_incoming_requests:
			bid_data.append(main_db.get_bid_data_by_bid_id(db_file, "BIDS_SUMMARY", incoming_request['BID_ID'])[0])
		dict_management.merge_list_of_dicts_on_key_assume_sorted_inplace(bid_data, bids_with_incoming_requests,
																		 key="BID_ID")




def send_you_have_no_incoming_requests(user_id):
	msg = "У вас пока нет запросов на обмен"
	bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_menu_start(user_id))


def send_you_have_x_incoming_requests(user_id, amount):
	msg = f"У вас {amount} {'запрос' if amount == 1 else 'запросов'} на обмен"
	bot.send_message(int(user_id), msg)
