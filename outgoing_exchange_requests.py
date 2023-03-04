import redis
from rq import Queue, Worker
from dotenv import dotenv_values
import telebot
import bot_markups as btmrkp
import main_db
import message_maker_request as mmr
from rq import job
import contacts

config = dotenv_values(".env")
print("\n\n\n\n\n")
API_KEY = config["API_KEY"]
REDIS_host = config["REDIS_host"]
REDIS_port = int(config["REDIS_port"])
REDIS_DB = int(config["REDIS_db"])
REDIS_QUEUE = int(config["REDIS_queue_db"])
forex_db = config["SQLITE_DB"]
print(f'Redis host is {REDIS_host}\n'
      f'redis port is {REDIS_port}\n'
      f'redis db is {REDIS_DB}\n')


bot = telebot.TeleBot(API_KEY)
r = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_DB, decode_responses=True)
r_queue = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_QUEUE)

Q_hi = Queue("Live interactions", connection=r_queue)
Q_lo = Queue("Requests", connection=r_queue)


"initial"
def check_terms(bid_to_request, user_id, db_file):
	msg = "Согласны на условия пользователя или хотите предложить свои?"
	bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_offer_terms_initial(user_id))
	pass


def send_message_after_request_to_bidder(user_id, bid_data_job_id):
	if len(job.Job.fetch(bid_data_job_id).result) == 1:
		msg = "Эта заявка больше не активна, выберите другую"
		bot.send_message(int(user_id), msg)
	else:
		msg = "Отправили запрос пользователю, когда он его примет, мы отправим вам его контакты"
		bot.send_message(int(user_id), msg)


def send_message_after_request_to_asker(bid_data_job_id, msg_job_id, bidder_id):
	if len(job.Job.fetch(bid_data_job_id).result) == 1:
		pass
	else:
		msg = job.Job.fetch(msg_job_id).result
		asker_id = job.Job.fetch(bid_data_job_id).result["USER_ID"]
		bot.send_message(int(asker_id), msg, reply_markup=btmrkp.markup_will_you_fulfill_request(asker_id, bidder_id))


def manage_askers_reply(askers_reply, bidder_id, asker_id, db_file, bid_data_job_id):
	bid_data = job.Job.fetch(bid_data_job_id).result
	bid_id = bid_data["BID_ID"]
	if askers_reply == "NO":
		msg = "Пользователь отказался от сделки"
		bot.send_message(bidder_id, msg)
		Q_hi.enqueue(main_db.clear_row, bid_id, "BID_ID_ASKERS", db_file, "PENDING_REQUESTS")
		Q_hi.enqueue(main_db.interaction_is_pending_with_bid_job, db_file, bid_data_job_id, "0")
	else:
		get_contacts_job = Q_hi.enqueue(main_db.get_contact_info, db_file, "USER_DATA_TABLE", asker_id)
		Q_hi.enqueue(main_db.update_db_value, db_file, "PENDING_REQUESTS", "BID_ID_ASKERS", bid_id, "ASKER_ID", asker_id)
		Q_hi.enqueue(contacts.check_contacts_in_exchange_request, bidder_id, asker_id, get_contacts_job.id, db_file,
					 depends_on=get_contacts_job)


def send_exchange_request(requested_bid, bidder_id, db_file):
	bid_data_job = Q_hi.enqueue(main_db.get_bid_data_by_bid_id, db_file, "ACTIVE_BIDS", requested_bid)
	msg_job = Q_hi.enqueue(mmr.message_for_incoming_request, bid_data_job.id, depends_on=bid_data_job)
	Q_hi.enqueue(send_message_after_request_to_bidder, bidder_id, bid_data_job.id)
	Q_hi.enqueue(send_message_after_request_to_asker, bid_data_job.id, msg_job.id, bidder_id, depends_on=msg_job)
	Q_hi.enqueue(main_db.store_pending_exchange_bid_and_bidder, db_file, requested_bid, bidder_id)
	Q_hi.enqueue(main_db.interaction_is_pending_with_bid_job, db_file, bid_data_job.id, "1", depends_on=bid_data_job)
