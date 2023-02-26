from rq import job, Queue, Worker
from dotenv import dotenv_values
import telebot
import redis
import re
import redis_db as rf
import bot_markups as btmrkp
import main_db

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


def contacts_is_complete(user_id, db_file):
	truth = main_db.get_val_db(db_file, "USER_DATA", "USER_ID", user_id, "CONTACT_DATA_COMPLETE")
	assert truth is None or truth is "1", f"res should be either None or 1 (input is {truth})"
	return True if truth else False


# todo
def view_my_contacts(user_id, db_file):
	get_contacts_job = Q_hi.enqueue(main_db.get_contact_info, db_file, "USER_DATA_TABLE", user_id)
	Q_hi.enqueue(check_contacts_in_menu, user_id, get_contacts_job.id, db_file, depends_on=get_contacts_job)


def check_contacts_in_new_bid(asker_id, get_contacts_job_id, db_file):
	contacts_data = job.Job.fetch(get_contacts_job_id).result
	assert isinstance(contacts_data, dict), f"contacts_data should be a dict (input is {contacts_data})"
	whatsapp = contacts_data["WHATSAPP_NUMBER"]
	telegram = contacts_data["TELEGRAM_NUMBER"]
	viber = contacts_data["VIBER_NUMBER"]
	local = contacts_data["LOCAL_NUMBER"]
	if whatsapp is None and telegram is None and viber is None and local is None:
		return False
	else:
		return True


def check_contacts_in_exchange_request(bidder_id, asker_id, get_contacts_job_id, db_file):
	contacts_data = job.Job.fetch(get_contacts_job_id).result
	assert isinstance(contacts_data, dict), f"contacts_data should be a dict (input is {contacts_data})"
	whatsapp = contacts_data["WHATSAPP_NUMBER"]
	telegram = contacts_data["TELEGRAM_NUMBER"]
	viber = contacts_data["VIBER_NUMBER"]
	local = contacts_data["LOCAL_NUMBER"]
	if whatsapp is None and telegram is None and viber is None and local is None:
		ask_for_contacts_in_exchange_request(asker_id)
	else:
		send_contacts_in_exchange_request(bidder_id, asker_id, get_contacts_job_id, db_file)


def check_contacts_in_menu(user_id, get_contacts_job_id, db_file):
	contacts_data = job.Job.fetch(get_contacts_job_id).result
	assert isinstance(contacts_data, dict), "contacts_data should be a dict"
	whatsapp = contacts_data["WHATSAPP_NUMBER"]
	telegram = contacts_data["TELEGRAM_NUMBER"]
	viber = contacts_data["VIBER_NUMBER"]
	local = contacts_data["LOCAL_NUMBER"]
	if whatsapp is None and telegram is None and viber is None and local is None:
		ask_for_contacts_in_menu(user_id)
	else:
		send_contacts_from_menu(user_id, db_file, get_contacts_job_id)


def ask_for_contacts_in_exchange_request(user_id):
	Q_hi.enqueue(rf.set_status, user_id, 20)
	msg = ("Необходимо заполнить контактные данные для отправки пользователю. "
		   "Нужен хотя бы один из видов связи:\n"
		   "whatsapp, telegram, viber или местный номер.\n"
		   "Указывайте номер с международным кодом а не внутренним.\n"
		   "Например +7 999 999 99 99 а не 8 999 999 99 99 для России\n")
	Q_hi.enqueue(bot.send_message, int(user_id), msg)
	ask_for_whatsapp(user_id)


def ask_for_contacts_in_menu(user_id):
	Q_hi.enqueue(rf.set_status, user_id, 10)
	msg = ("Необходимо заполнить контактные данные для отправки пользователю. "
		   "Нужен хотя бы один из видов связи:\n"
		   "whatsapp, telegram, viber или местный номер.\n"
		   "Указывайте номер с международным кодом а не внутренним.\n"
		   "Например +7 999 999 99 99 а не 8 999 999 99 99 для России\n")
	Q_hi.enqueue(bot.send_message, int(user_id), msg)
	ask_for_whatsapp(user_id)


def ask_for_whatsapp(user_id):
	msg = ("Укажите номер используемый в Whatsapp. Для пропуска укажите 0")
	Q_hi.enqueue(bot.send_message, int(user_id), msg)


def ask_for_telegram(user_id):
	msg = ("Укажите номер используемый в Telegram. Для пропуска укажите 0")
	Q_hi.enqueue(bot.send_message, int(user_id), msg)


def ask_for_viber(user_id):
	msg = ("Укажите номер используемый в Viber. Для пропуска укажите 0")
	Q_hi.enqueue(bot.send_message, int(user_id), msg)


def ask_for_local_number(user_id):
	msg = ("Укажите мечтный номер используемый в Стране. Для пропуска укажите 0")
	Q_hi.enqueue(bot.send_message, int(user_id), msg)


def store_whatsapp_number(number, user_id, db_file):
	Q_hi.enqueue(rf.incr_by, user_id, "STATUS", 1)
	if number == "0":
		ask_for_telegram(user_id)
	else:
		formatted_number = format_number(number)
		Q_hi.enqueue(main_db.update_db_value, db_file, "USER_DATA_TABLE", "WHATSAPP_NUMBER", user_id, formatted_number)
		ask_for_telegram(user_id)


def store_telegram_number(number, user_id, db_file):
	Q_hi.enqueue(rf.incr_by, user_id, "STATUS", 1)
	if number == "0":
		ask_for_viber(user_id)
	else:
		formatted_number = format_number(number)
		Q_hi.enqueue(main_db.update_db_value, db_file, "USER_DATA_TABLE", "TELEGRAM_NUMBER", user_id, formatted_number)
		ask_for_viber(user_id)


def store_viber_number(number, user_id, db_file):
	Q_hi.enqueue(rf.incr_by, user_id, "STATUS", 1)
	if number == "0":
		ask_for_local_number(user_id)
	else:
		formatted_number = format_number(number)
		Q_hi.enqueue(main_db.update_db_value, db_file, "USER_DATA_TABLE", "VIBER_NUMBER", user_id, formatted_number)
		ask_for_local_number(user_id)


def store_local_number_from_menu(number, user_id, db_file):
	Q_hi.enqueue(rf.incr_by, user_id, "STATUS", 1)
	if number == "0":
		ask_for_telegram(user_id)
	else:
		formatted_number = format_number(number)
		Q_hi.enqueue(main_db.update_db_value, db_file, "USER_DATA_TABLE", "LOCAL_NUMBER", user_id, formatted_number)
		get_contacts_job = Q_hi.enqueue(main_db.get_contact_info, db_file, "USER_DATA_TABLE", user_id)
		Q_hi.enqueue(check_contacts_in_menu, user_id, get_contacts_job.id, db_file, depends_on=get_contacts_job)


def store_local_number_in_exchange_request(number, user_id, db_file):
	Q_hi.enqueue(rf.incr_by, user_id, "STATUS", 1)
	if number == "0":
		ask_for_telegram(user_id)
	else:
		formatted_number = format_number(number)
		Q_hi.enqueue(main_db.update_db_value, db_file, "USER_DATA_TABLE", "LOCAL_NUMBER", user_id, formatted_number)


def format_number(number):
	formatted_number = re.sub(r'[^0-9]+', '', number)
	return "+" + formatted_number


def send_contacts_in_exchange_request(bidder_id, asker_id, get_contacts_job_id, db_file):
	msg = "Эти данные отправим:\n"
	msg2bidder = "Контактные данные пользователя:\n"
	msg_job = Q_hi.enqueue(make_contacts_message, get_contacts_job_id)
	Q_hi.enqueue(send_message_for_self_in_exchange_request, asker_id, msg, msg_job.id, depends_on=msg_job)
	if bidder_id == False:
		bidder_id_job = Q_hi.enqueue(main_db.get_val_db_order_by, db_file, "PENDING_REQUESTS", "ASKER_ID", asker_id,
									 "BIDDER_ID", "REQUEST_DATE")
		Q_hi.enqueue(send_message_for_bidder_in_exchange_request_with_job, bidder_id_job.id, msg2bidder, msg_job.id,
					 depends_on=bidder_id_job)
	else:
		Q_hi.enqueue(send_message_for_bidder_in_exchange_request, bidder_id, msg2bidder, msg_job.id, depends_on=msg_job)


def send_contacts_from_menu(user_id, db_file,  get_contacts_job_id):
	msg = "Записали данные:\n"
	msg_job = Q_hi.enqueue(make_contacts_message, get_contacts_job_id)
	Q_hi.enqueue(send_message_for_self_from_menu, user_id, msg, msg_job.id, depends_on=msg_job)


def make_contacts_message(get_contacts_job_id):
	contacts_data = job.Job.fetch(get_contacts_job_id).result
	whatsapp = contacts_data["WHATSAPP_NUMBER"]
	telegram = contacts_data["TELEGRAM_NUMBER"]
	viber = contacts_data["VIBER_NUMBER"]
	local = contacts_data["LOCAL_NUMBER"]
	nl = "\n"
	msg = (f"{'WhatsApp: ' + whatsapp + nl if whatsapp is not None else ''}"
		   f"{'Telegram: ' + telegram + nl if telegram is not None else ''}"
		   f"{'Viber: ' + viber + nl if viber is not None else ''}"
		   f"{'Local number: ' + local + nl if local is not None else ''}")
	return msg


def send_message_for_self_from_menu(user_id, msg_front, msg_job):
	msg = msg_front + job.Job.fetch(msg_job).result
	bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_menu_start(user_id))


def send_message_for_self_in_exchange_request(user_id, msg_front, msg_job_id):
	msg = msg_front + job.Job.fetch(msg_job_id).result
	bot.send_message(int(user_id), msg)


def send_message_for_bidder_in_exchange_request(user_id, msg_front, msg_job_id):
	msg = msg_front + job.Job.fetch(msg_job_id).result
	bot.send_message(int(user_id), msg)


def send_message_for_bidder_in_exchange_request_with_job(user_id_job_id, msg_front, msg_job_id):
	user_id = job.Job.fetch(user_id_job_id).result
	msg = msg_front + job.Job.fetch(msg_job_id).result
	bot.send_message(int(user_id), msg)
