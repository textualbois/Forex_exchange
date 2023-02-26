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

"""
connect SQL DB
"""


@bot.message_handler(commands=['Start', "start"])
def start(message):
    Q_hi.enqueue(rf.start_user, message.chat.id)
    bot.send_message(message.chat.id, "Найти обмен - бот для поиска \
                                          контр-агента по обмену денег \n\
        Бот не является гарантом: безопасность вас и ваших средств лежит на вас. \n\
        Выберите действие:... \n",
                     reply_markup=btmrkp.markup_menu_start(message.chat.id))


"""
добавить оьмен в свой коллбэк (добавить reply_markup к старт)
"""
@bot.message_handler(commands=['обмен'])
def obmen(message):
    msg = "Выберите валюту для получения:"  # "Выберите валюту для получения:" "Какая валюта тебе нужна?"
    bot.send_message(message.chat.id, msg, reply_markup=btmrkp.markup_need_currency(message.chat.id))
"""
добавить обмен в свой коллбэк
"""


def reply_to_mainmenu(user_id):
    msg = "Основное меню"
    bot.send_message(int(user_id), msg,
                     reply_markup=btmrkp.markup_menu_start(user_id))


# 0 stores start data, sends to needed currency
def reply_to_newbid(user_id, db_file):
    print("replying to newbid query")
    contacts_is_complete_job = Q_hi.enqueue(contacts.is_complete, user_id, db_file)
    active_bid_count_job = Q_hi.enqueue(main_db.get_active_bids_count, db_file, user_id)
    Q_hi.enqueue(check_bids_and_contacts, user_id, db_file, active_bid_count_job.id,
                 depends_on=active_bid_count_job)


# 0.1 checks for contact data
def check_bids_and_contacts(user_id, db_file, active_bids_count_job):
    print(f"checking bid count and contact info for {user_id}")
    active_bid_count_dict = job.Job.fetch(active_bids_count_job).result[0]
    assert isinstance(active_bid_count_dict, dict), "active_bid_count_dict should be a dict"
    active_bid_count = active_bid_count_dict["ACTIVE_BIDS_COUNT"]
    print(f"active_bid_count is {active_bid_count}")
    if int(active_bid_count) == 0:
        get_contacts_job = Q_hi.enqueue(main_db.get_contact_info, db_file, "USER_DATA", user_id)
        print("111111111111111111")
        check_contacts_job = Q_hi.enqueue(contacts.check_contacts_in_new_bid, user_id, get_contacts_job.id, db_file,
                                          depends_on=get_contacts_job)
        print("222222222222222222")
        Q_hi.enqueue(start_new_bid_with_contact_check, user_id, db_file, check_contacts_job.id, depends_on=check_contacts_job)
    else:
        Q_hi.enqueue(start_new_bid, user_id, db_file)


# 0.2 asks for contacts data or starts a new bid
def start_new_bid_with_contact_check(user_id, db_file, check_contacts_job_id):
    has_contacts = job.Job.fetch(check_contacts_job_id).result
    if has_contacts:
        print(f'getting status hash data {rf.read_hash(user_id, "STATUS")}')
        Q_hi.enqueue(rf.start_user, user_id)
        print(f'Юзеру {user_id} начал новую заявку')
        msg = "Выберите валюту для получения:"  # "Выберите валюту для получения:"  "Какая валюта тебе нужна?"
        bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_need_currency(user_id))
    else:
        msg = ("Для добавления дополнительных заявок необходимо ввести свои данные. Это необходимо для того, "
               "чтобы пользователь мог откликнуться на вашу заявку. Прежде чем передавать ваши данные другому "
               "пользователю мы будем также спрашивать вашего разрешения и актуальности заявки.")
        bot.send_message(int(user_id), msg)
        contacts.ask_for_contacts_in_menu(user_id)


# 0.3
def start_new_bid(user_id, db_file):
    print(f'getting status hash data {rf.read_hash(user_id, "STATUS")}')
    Q_hi.enqueue(rf.start_user, user_id)
    print(f'Юзеру {user_id} начал новую заявку')
    msg = "Выберите валюту для получения:"  # "Выберите валюту для получения:"  "Какая валюта тебе нужна?"
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_need_currency(user_id))


# 1 stores needed currency, asks how the user wants to receive it
def reply_to_get(markup_result, user_id):
    print(f'getting status hash data {rf.read_hash(user_id, "STATUS")}')
    print(f'Юзеру {user_id} нужны {markup_result}')
    Q_hi.enqueue(rf.update_hash, user_id, "NEED_CUR", markup_result, 2)
    msg = "Как хотите получить деньги?:"  # "Как хочешь получить деньги?"
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_receive(user_id))


# 2 stores user's way to receive money, asks what currency the user has
def reply_to_rec(markup_result, user_id):
    print(f'getting status hash data {rf.read_hash(user_id, "STATUS")}')
    print(f'Юзер {user_id} хочет получить их в/на {markup_result}')
    Q_hi.enqueue(rf.update_hash, user_id, "NEED_LOC", markup_result, 3)
    msg = "Какая у вас валюта?:"  # "Какая у тебя валюта?"
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_what_u_got(user_id))


# 3 stores user's available currency, asks where he has it(cash, card)
def reply_to_has(markup_result, user_id):
    print(f'getting status hash data {rf.read_hash(user_id, "STATUS")}')
    print(f'У Юзера {user_id} есть {markup_result}')
    Q_hi.enqueue(rf.update_hash, user_id, "HAS_CUR", markup_result, 4)
    msg = "Как можете передать средства?:"  # "Как можешь средства передать?"
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_how_u_send(user_id))


# 4 stores user's money location(cash, card), asks how much he wants to change in HIS currency
def reply_to_from(markup_result, user_id):
    print(f'getting status hash data {rf.read_hash(user_id, "STATUS")}')
    print(f'Юзер {user_id} может передать через {markup_result}')
    Q_hi.enqueue(rf.update_hash, user_id, "HAS_LOC", markup_result, 5)
    msg = f'Введите сумму {rf.read_hash(user_id,"HAS_CUR")} для обмена:\n'\
          f'Введите 0 для пропуска шага'  # 'сколько есть'
    bot.send_message(int(user_id), msg)


# 5 checks if user's reply is a number, stores it, asks how much he wants in return
def reply_to_has_val(message, user_id):
    user_msg = message.text
    print(f'Юзер {user_id} ответил {user_msg} ')
    if "".join(user_msg.split()).isdigit():
        Q_hi.enqueue(rf.update_hash, user_id, "HAS_VAL", "".join(user_msg.split()), 6)
        msg = f'Введите сумму {rf.read_hash(user_id, "NEED_CUR")} которую хотите получить:\n' \
              f'Введите 0 для пропуска шага'  # 'сколько нужно'
        bot.send_message(user_id, msg)
    else:
        bot.send_message(user_id, "Введите целое число, например 123456")


# 6 checks if user's reply is a number, stores it, asks his location
def reply_to_need_val(message, user_id):
    user_msg = message.text
    if "".join(user_msg.split()).isdigit():
        Q_hi.enqueue(rf.update_hash, user_id, "NEED_VAL", "".join(user_msg.split()), 7)
        msg = ("Давайте добавим местоположение, где вам будет удобно произвести обмен.\n\n"
               "Бот принимает координаты, например:\n"
               "28.399471, -14.155266\n"
               "Это координаты Канарских Островов\n\n"
               "1) В любом приложении карт отметьте точку на карте, "
               "в описании этой точки будет похожий набор цифр.\n"
               "2) скопируйте его и вставьте ниже.\n\n"
               "Если не получается, отправьте любое сообщение.")
        bot.send_message(user_id, msg)
    else:
        bot.send_message(user_id, "Введите целое число, например 123456")


# 7.A check if user location is valid
def location_is_valid(location):
    regex_lat = r'^(\+|-)?(?:90(?:(?:\.0{1,7})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,7})?))$'
    regex_lon = r'^(\+|-)?(?:180(?:(?:\.0{1,7})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,7})?))$'
    if len(location) == 2:
        if re.match(regex_lat, location[0]) and re.match(regex_lon, location[1]):
            return True
    else:
        return False


# 7.B sends instructions for user's location data
# TODO
def send_video_instructions(user_id):
    pass


# 7 stores user's coordinates, prompts to add an alias for them
def reply_to_main_loc_coordinates(message, user_id):
    location = (re.sub(r"[\r\n\s\(\)]+", "", message.text)).split(",")
    print(f'Юзер {user_id} ввел {location}')
    if location_is_valid(location):
        Q_hi.enqueue(rf.update_hash, user_id, "LOC_MAIN_LAT", location[0], 8)
        Q_hi.enqueue(rf.update_hash, user_id, "LOC_MAIN_LON", location[1], 8)
        msg = ("Добавьте название этой локации, например:\n"
               "Стамбул, Таксим\nили\nАнталья")
        bot.send_message(user_id, msg)
    else:
        msg = ("Бот не распознал локацию\n"
               "Сейчас направим короткие видео инструкции")
        bot.send_message(user_id, msg)
        send_video_instructions(user_id)


# 8 stores user's location alias, asks user to check results
def reply_to_main_loc_alias(message, user_id):
    user_msg = (re.sub(r"[\r\n]+", " ", message.text)).rstrip()
    print(f'Юзер {user_id} назвал локацию {user_msg}')
    Q_hi.enqueue(rf.update_hash, user_id, "LOC_MAIN_ALIAS", user_msg, 9)
    Q_hi.enqueue(rf.send_check_result, user_id)


# 9 handles user response to input check, see 9A, 9B and 9C lower
# TODO
def reply_to_check(markup_result, user_id, db_file):
    print(f'Юзер {user_id} проверяет свой ввод')
    if markup_result == "OK":
        check_result_ok(user_id, db_file)
    elif markup_result == "USERBAD":
        check_result_userbad(user_id)
    elif markup_result == "BOTBAD":
        check_result_botbad(user_id)

        pass
        """
        accept feedback
        start over
        """


# 9A stores user input and sends it to main db
def check_result_ok(user_id, db_file):
    msg = ("Фиксируем заявку..\n Скоро сможете просмотреть ее в разделе мои заявки "
           "и просмотреть чужие заявки подходящие под ваши")
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_menu_start(user_id))
    Q_lo.enqueue(rf.transfer_to_main_db, user_id, db_file)


# 9B
def check_result_userbad(user_id):
    Q_hi.enqueue(rf.start_user, user_id)
    msg = "Попробуем ещё раз.\n Какую валюту хотите получить:"
    # "Выберите валюту для получения:" "Какая валюта тебе нужна?"
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_need_currency(user_id))


# 9C
# TODO
def check_result_botbad(user_id):
    msg = ()
    pass
    """
    accept feedback
    start over
    """


# B1
def reply_to_mybids(user_id):
    msg = "Какие заявки хотите просмотреть?:"
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_my_bids(user_id))


# B2
def reply_to_whatbids(markup_result, user_id, db_file):
    Q_hi.enqueue(rf.reset_shown_data_count, user_id)  # makes sure the user is active in redis
    if markup_result == "ACTIVE":
        job1 = Q_hi.enqueue(rf.move_from_main_db, user_id, "USER_ID", "ACTIVE_BIDS_COUNT", db_file, "USER_DATA")
        wait_for_result(job1)
        msg = (f"У вас {job1.result} активных заявок")
        bot.send_message(int(user_id), msg)
        if job1.result != 0:
            show_my_active_bids(user_id, db_file)
        else:
            reply_to_mybids(int(user_id))
    elif markup_result == "FULFILLED":
        job1 = Q_hi.enqueue(rf.move_from_main_db, user_id, "USER_ID", "FULFILLED_BIDS_COUNT", db_file, "USER_DATA")
        wait_for_result(job1)
        msg = (f"У вас {job1.result} исполненных заявок")
        bot.send_message(int(user_id), msg)
        if job1.result != 0:
            show_my_fulfilled_bids(user_id, db_file)
        else:
            reply_to_mybids(int(user_id))
    elif markup_result == "CANCELLED":
        job1 = Q_hi.enqueue(rf.move_from_main_db, user_id, "USER_ID", "CANCELLED_BIDS_COUNT", db_file, "USER_DATA")
        wait_for_result(job1)
        msg = (f"У вас {job1.result} удаленных заявок")
        bot.send_message(int(user_id), msg)
        if job1.result != 0:
            show_my_cancelled_bids(user_id, db_file)
        else:
            reply_to_mybids(int(user_id))


# THREE FUNCTIONS BELLOW SHOULD:
# FIGURE OUT AMOUNT OF BIDS,
# FIGURE OUT HOW MANY ARE CURRENTLY SHOWN
# MAKE A MESSAGE OF THE NEXT FEW BIDS
# DISPLAY THEM THROUGH A CALL TO BOT_MARKUPS
# B3.a
def show_my_active_bids(user_id, db_file):
    active_bids_count = rf.read_hash(user_id, "ACTIVE_BIDS_COUNT")
    shown_data_job = Q_hi.enqueue(rf.read_hash, user_id, "SHOWN_DATA")
    #wait_for_result(shown_data_job) #return if works buggy
    print(f"user {user_id}"
          f"current active bids count: {active_bids_count}\n"
          f"bids shown to user: {shown_data_job.result}")
    get_bids_job = Q_hi.enqueue(main_db.get_bids_for_message,
                                db_file, "ACTIVE_BIDS", int(user_id), shown_data_job.id, 3,
                                depends_on=shown_data_job)
    msg_job = Q_hi.enqueue(mm.show_bids, get_bids_job.id, shown_data_job.id, depends_on=get_bids_job)
    wait_for_result(get_bids_job) #possibly remove later and add depends_on argument above
    print(f"{user_id} amount of bids pulled by request {len(get_bids_job.result)}")
    bid_id_list = [bid["BID_ID"] for bid in get_bids_job.result]
    print(f"bid_id_list:")
    print(bid_id_list)
    wait_for_result(msg_job)
    msg = msg_job.result
    if int(shown_data_job.result) + len(get_bids_job.result) < int(active_bids_count):
        bot.send_message(int(user_id), msg,
                         reply_markup=btmrkp.markup_my_active(user_id, bid_id_list, int(shown_data_job.result),
                                                              show_more=True))
        Q_hi.enqueue(rf.incr_by, user_id, "SHOWN_DATA", len(get_bids_job.result))
    else:
        bot.send_message(int(user_id), msg,
                         reply_markup=btmrkp.markup_my_active(user_id, bid_id_list, int(shown_data_job.result),
                                                              show_more=False))


# TODO
# B3.b
def show_my_cancelled_bids(user_id, db_file):
    cancelled_bids_count = rf.read_hash(user_id, "CANCELLED_BIDS_COUNT")
    shown_data_job = Q_hi.enqueue(rf.read_hash, user_id, "SHOWN_DATA")
    #wait_for_result(shown_data_job) return if works buggy
    print(f"user {user_id}"
          f"current cancelled bids count: {cancelled_bids_count}\n"
          f"bids shown to user: {shown_data_job.result}")
    get_bids_job = Q_hi.enqueue(main_db.get_bids_for_message_cancelled_or_fulfilled,
                                db_file, "BID_SUMMARY", int(user_id), shown_data_job.id, 3, "CANCELLED_BIDS",
                                depends_on=shown_data_job)
    msg_job = Q_hi.enqueue(mm.show_bids, get_bids_job.id, shown_data_job.id, depends_on=get_bids_job)
    wait_for_result(get_bids_job) #possibly remove later and add depends_on argument above
    print(f"{user_id} amount of bids pulled by request {len(get_bids_job.result)}")
    bid_id_list = [bid["BID_ID"] for bid in get_bids_job.result]
    wait_for_result(msg_job)
    msg = msg_job.result
    if int(shown_data_job.result) + len(get_bids_job.result) < int(cancelled_bids_count):
        bot.send_message(int(user_id), msg,
                         reply_markup=btmrkp.markup_my_cancelled(user_id, bid_id_list, int(shown_data_job.result),
                                                                 show_more=True))
        Q_hi.enqueue(rf.incr_by, user_id, "SHOWN_DATA", len(get_bids_job.result))
    else:
        bot.send_message(int(user_id), msg,
                         reply_markup=btmrkp.markup_my_cancelled(user_id, bid_id_list, int(shown_data_job.result),
                                                                 show_more=False))


# TODO
# B3.c
def show_my_fulfilled_bids(user_id, db_file, fulfilled_bids):
    pass


def request_to_remove_bid(bid_id, user_id, db_file):
    msg = "Закрываем выбранную заявку..\n"
    bot.send_message(int(user_id), msg)
    Q_lo.enqueue(main_db.move_bid_to_cancelled, bid_id, user_id, db_file)


def wait_for_result(job):
    while job.result == None:
        time.sleep(2)