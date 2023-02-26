import time
import redis
from rq import Queue, Worker
from dotenv import dotenv_values
import telebot
from telebot import types
import sqlite3
from rq import job
import main_db
import redis_db as rf
import bot_markups as btmrkp
import re
import message_maker as mm
import message_maker_matching_bids as mmmb

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


def show_exit_or_request(markup_result, user_id, db_file):
	if markup_result == "SHOWMORE":
		show_matches(user_id)
	elif markup_result == "EXIT":
		exit_matching(user_id, db_file)
	else:
		send_exchange_request(markup_result, user_id, db_file)


def ask_range(bid_id, user_id, db_file):
	Q_hi.enqueue(rf.store_new_search, user_id, bid_id)
	Q_hi.enqueue(rf.reset_shown_data_count, user_id)
	msg = "Выберите радиус поиска встречных заявок в километрах"
	bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_search_range(user_id))


# A
def setup_matching_bids(search_range, user_id, db_file):
	# constraints_for_query saves the constraints to the redis DB AND returns the bid_id.
	# todo refactor rf.complete_search_data to return a dictionary of the constraints.
	#  maybe no need to store the constraints
	constraints_for_query_job = Q_hi.enqueue(rf.complete_search_data, search_range, user_id, db_file)
	matching_bid_ids_job = Q_hi.enqueue(main_db.get_list_of_matching_bid_ids, db_file, "ACTIVE_BIDS", user_id,
										constraints_for_query_job.id, depends_on=constraints_for_query_job)
	store_matching_bids_job = Q_hi.enqueue(rf.store_bids_that_match, user_id, matching_bid_ids_job.id,
								  depends_on=matching_bid_ids_job)
	show_matches(user_id, db_file)


# todo
# todo
# todo
# B
def show_matches(user_id, db_file):
	matching_bids_count_job = Q_hi.enqueue(rf.redis_list_length, f"matches_for_{user_id}")
	shown_data_job = Q_hi.enqueue(rf.read_hash, user_id, "SHOWN_DATA")
	trimmed_bid_id_list_job = Q_hi.enqueue(rf.get_trimmed_list, user_id, shown_data_job.id, 3,
										   depends_on=shown_data_job)
	get_bids_for_msg_job = Q_hi.enqueue(main_db.get_bids_for_message_that_match, db_file, "ACTIVE_BIDS",
										trimmed_bid_id_list_job.id, depends_on=trimmed_bid_id_list_job)
	msg_job = Q_hi.enqueue(mmmb.show_bids, get_bids_for_msg_job.id, shown_data_job.id,
						   depends_on=get_bids_for_msg_job)
	Q_hi.enqueue(send_matches, user_id, msg_job.id, shown_data_job.id, trimmed_bid_id_list_job.id,
				 matching_bids_count_job.id, depends_on=msg_job)


# C
def send_matches(user_id, msg_job_id, shown_data_job_id, bid_id_list_job_id, matching_bids_count_job_id):
	matching_bids_count = job.Job.fetch(matching_bids_count_job_id).result
	bid_id_list = job.Job.fetch(bid_id_list_job_id).result
	shown_bids_count = int(job.Job(shown_data_job_id).result)
	msg = job.Job(msg_job_id).result
	print(f"msg:\n"
		  f"{msg}\n")
	print(f"user {user_id}\n"
		  f"matching bids count: {matching_bids_count}\n"
		  f"bids shown to user: {shown_bids_count}\n")
	print(f"matching bids ids:")
	print(bid_id_list)
	if shown_bids_count + len(bid_id_list) < int(matching_bids_count):
		bot.send_message(int(user_id), msg,
						 reply_markup=btmrkp.markup_matching_bids(user_id, bid_id_list, shown_bids_count,
															  show_more=True))
		Q_hi.enqueue(rf.incr_by, user_id, "SHOWN_DATA", len(bid_id_list))
	else:
		bot.send_message(int(user_id), msg,
						 reply_markup=btmrkp.markup_matching_bids(user_id, bid_id_list, shown_bids_count,
															  show_more=False))

# TODO
def exit_matching(user_id, db_file):
	Q_hi.enqueue(rf.block_search, user_id)
	# GoTo start menu
	pass


# TODO
def send_exchange_request(matched_bid_id, user_id, db_file):
	pass