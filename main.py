import time
import redis
from rq import Queue, Worker
from dotenv import dotenv_values
import telebot
from telebot import types
import sqlite3
import create_db_byAI
import main_db
import datetime
import pytz
import outgoing_exchange_requests
import matching_bids
import project_time_functions as ptf
import redis_db as rf
import bot_markups as btmrkp
import user_replies as ur
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

create_db_byAI.connect_and_create(forex_db)

bot = telebot.TeleBot(API_KEY)
r = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_DB, decode_responses=True)
r_queue = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_QUEUE)

Q_hi = Queue("Live interactions", connection=r_queue)
Q_lo = Queue("Requests", connection=r_queue)


@bot.message_handler(commands=['Start', 'start'])
def start(message):
    user_id = message.chat.id
    current_time = ptf.get_current_time()
    Q_hi.enqueue(rf.start_user, user_id)
    Q_hi.enqueue(main_db.insert_new_user, forex_db, "USER_DATA", user_id, current_time)
    msg = ("Найти обмен - бот для поиска "
           "контр-агента по обмену денег\n"
           "Бот не является гарантом: безопасность "
           "вас и ваших средств лежит на вас.\n"
           "Выберите действие:... \n")
    bot.send_message(user_id, msg, reply_markup=btmrkp.markup_menu_start(user_id))


"""
добавить обмен в свой коллбэк (добавить reply_markup к старт)
"""
@bot.message_handler(commands = ['обмен'])
def obmen(message):
    user_id = message.chat.id
    msg = "Какую валюту хотите получить:" #"Выберите валюту для получения:"  "Какая валюта тебе нужна?"
    bot.send_message(user_id, msg, reply_markup=btmrkp.markup_need_currency(user_id))
"""
добавить оьмен в свой коллбэк
"""


@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    print(call.data)
    # add markup split by stages to have less repetitive if statement executions
    markup_identity = call.data.split("_")[0]
    markup_result = call.data.split("_")[1]
    user_id = call.message.chat.id
    message_id = call.message.id
    markup_result2 = call.data.split("__")[1]
    print(user_id)
    clear_inline_keyboard(user_id, message_id)
    if markup_identity == "MAINMENU":
        ur.reply_to_mainmenu(user_id)
    elif markup_identity == "NEWBID":  # 0
        ur.reply_to_newbid(user_id, forex_db)
    elif markup_identity == "GET":  # 1
        ur.reply_to_get(markup_result, user_id)  # goes to rec
    elif markup_identity == "REC":  # 2
        ur.reply_to_rec(markup_result, user_id)  # goes to has
    elif markup_identity == "HAS":  # 3
        ur.reply_to_has(markup_result, user_id)  # goes to from
    elif markup_identity == "FROM":  # 4
        ur.reply_to_from(markup_result, user_id)  # goes to status check (has_val)
    elif markup_identity == "CHECK":  # 9
        ur.reply_to_check(markup_result, user_id, forex_db)
    elif markup_identity == "MYBIDS":  # B1
        ur.reply_to_mybids(user_id)  # ask which of his bids user wants to view (WHATBIDS)
    elif markup_identity == "WHATBIDS":  # B2
        ur.reply_to_whatbids(markup_result, user_id, forex_db)  #
    elif markup_identity == "MYACTIVEBIDS":  # B3.a
        ur.show_my_active_bids(user_id, forex_db)
   # elif markup_identity == "MYFULFILLEDBIDS":  # B3.b
   #     ur.reply_to_myfulfilledbids(markup_result, user_id, forex_db)
    elif markup_identity == "MYCANCELLEDBIDS":  # B3.c
        ur.show_my_cancelled_bids(user_id, forex_db)

    elif markup_identity == "DELETEBID":
        ur.request_to_remove_bid(markup_result, user_id, forex_db)

    elif markup_identity == "MATCHTHISBID":
        matching_bids.ask_range(markup_result, user_id, forex_db)

    #elif markup_identity == "OTHERSBIDS":
    #    ur.reply_to_otherbids(markup_result, user_id, forex_db)
    #elif markup_identity == "OTHERSBIDSNEEDCUR":
    #    ur.reply_to_othersbis(markup_result, user_id, forex_db)
    #elif markup_identity == "OTHERSBIDSHASCUR":
    #    ur.reply_to_othersbis(markup_result, user_id, forex_db)
    #elif markup_identity == "OTHERSBIDSNEEDLOC":
    #    ur.reply_to_othersbis(markup_result, user_id, forex_db)
    #elif markup_identity == "OTHERSBIDSNEEDHAS":
    #    ur.reply_to_othersbis(markup_result, user_id, forex_db)

    elif markup_identity == "SEARCHRANGE":
        matching_bids.setup_matching_bids(int(markup_result), user_id, forex_db)
    elif markup_identity == "MYBIDMATCHES":
        matching_bids.show_matches(user_id, forex_db)

    elif markup_identity == "SENDEXCHANGEREQUEST":
        outgoing_exchange_requests.send_exchange_request(markup_result, user_id, forex_db)
    elif markup_identity == "REPLYTOREQUEST":
        outgoing_exchange_requests.manage_askers_reply(markup_result, markup_result2, user_id, forex_db)
   # elif markup_identity == "MAKINGOFFER":
   #     outgoing_exchange_requests.send_request(markup_result, user_id, forex_db)

    #elif markup_identity == "OTHERSBIDS":
    #    ur.reply_to_otherbids(markup_result, user_id, forex_db)
    #elif markup_identity == "FEEDBACK":
    #    ur.reply_to_feedback(markup_result, user_id)
    elif markup_identity == "CONTACTSMENU":
        bot.send_message(int(user_id), "Меню контактов", btmrkp.markup_my_contacts(user_id))
    elif markup_identity == "VIEWCONTACTS":
        contacts.view_my_contacts(user_id, forex_db)
    elif markup_identity == "ADDCONTACTS":
        contacts.ask_for_contacts_in_menu(user_id)

@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    user_id = message.chat.id
    status = int(rf.read_hash(user_id, "STATUS"))
    print(f'getting status hash data {status}')
    if status < 10:
        if status == 5:  # 5
            ur.reply_to_has_val(message, user_id)  # goes to status check (need_val)
        elif status == 6:  # 6
            ur.reply_to_need_val(message, user_id)  # goes to status check (main loc coordinates)
        elif status == 7:  # 7:
            ur.reply_to_main_loc_coordinates(message, user_id)  # goes to status check (main loc alias)
        elif status == 8:  # 8:
            ur.reply_to_main_loc_alias(message, user_id)
    elif status < 20:
        if status == 10:
            contacts.store_whatsapp_number(message, user_id, forex_db)
        elif status == 11:
            contacts.store_telegram_number(message, user_id, forex_db)
        elif status == 12:
            contacts.store_viber_number(message, user_id, forex_db)
        elif status == 13:
            contacts.store_local_number_from_menu(message, user_id, forex_db)
    elif status < 30:
        if status == 20:
            contacts.store_whatsapp_number(message, user_id, forex_db)
        elif status == 21:
            contacts.store_telegram_number(message, user_id, forex_db)
        elif status == 22:
            contacts.store_viber_number(message, user_id, forex_db)
        elif status == 23:
            contacts.store_local_number_in_exchange_request(message, user_id, forex_db)


def clear_inline_keyboard(user_id, msg_id):
    bot.edit_message_reply_markup(chat_id=int(user_id),message_id=int(msg_id), reply_markup=None)

bot.polling()