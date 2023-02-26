import os
import telebot
from dotenv import dotenv_values
import sqlite3
from sqlite3 import Error

config = dotenv_values(".env")
print("\n\n\n\n\n")
API_KEY = config["API_KEY"]

bot = telebot.TeleBot(API_KEY)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_new_user(conn,table,prime_key,username,menu_pos=0,\
                    TTL_BIDS=0,ACTIVE_BIDS=0,Good_BIDS=0,CANC_BIDS=0):
    query=f'INSERT if NOT EXIST INTO {table} (ID,USERNAME,MENU_POS,TTL_BIDS,ACTIVE_BIDS,Good_BIDS,CANC_BIDS) \
        VALUES ({prime_key},{username},{menu_pos},{TTL_BIDS},{ACTIVE_BIDS},{Good_BIDS},{CANC_BIDS})'
    conn.execute(query)

def insert_new_temp_bid(conn,table,prime_key,NEED_CUR="",
                    NEED_LOC="",HAS_CUR="",HAS_LOC="",
                    NEED_VAL=0,HAS_VAL=0,R1=0,R2=0,status=0):
    query=f'INSERT or REPLACE INTO {table} (ID,NEED_CUR,NEED_LOC,HAS_CUR,HAS_LOC,NEED_VAL,HAS_VAL,R1,R2,status) \
        VALUES ({prime_key},{NEED_CUR},{NEED_LOC},{HAS_CUR},{HAS_LOC},{NEED_VAL},{HAS_VAL},{R1},{R2},{status})'
    conn.execute(query)

#def insert_row(conn,table,prime_key,column,status_column = "STATUS",status = 0):
#    query = f'INSERT or IGNORE INTO {table}({column}) VALUES({prime_key})'
#    conn.execute(query)
#    query = f'UPDATE {table} \
#        SET {status_column} = 0 \
#            WHERE \
#                {column} = {prime_key}'


def update_db_value(conn,table,prime_key,column,new_value):
    query = f'UPDATE {table} \
        SET {column} = {new_value} \
        WHERE \
            ID = {prime_key}'
    conn.execute(query)

def get_val_db(conn,table,prime_key,column):
    query = f'SELECT {column} FROM {table}\
    WHERE \
        ID = {prime_key}'
    conn.execute(query)
    return (conn.fetchall())[0]

db_conn = create_connection("forex_obmen_db.db")
sql_main(db_conn)


def markup_need_currency(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Рубли/RUB", callback_data = "GET_RUB___" + str(chatId)),
        InlineKeyboardButton("Лиры/TRL", callback_data = "GET_TRL___" + str(chatId))
    )
    return markup

def markup_receive(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("На Рус. карту", callback_data = "REC_RU___" + str(chatId)),
        InlineKeyboardButton("На Тур. карту", callback_data = "REC_TR___" + str(chatId))
    )
    markup.add(
        InlineKeyboardButton("Наличкой", callback_data = "REC_NAL___" + str(chatId))
    )
    return markup

def markup_how_u_send(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Перевод с Рус. карты", callback_data = "FROM_RU___" + str(chatId)),
        InlineKeyboardButton("Перевод с Тур. карты", callback_data = "FROM_TR___" + str(chatId))
    )
    markup.add(
        InlineKeyboardButton("Передам наличкой", callback_data = "FROM_NAL___" + str(chatId))
    )
    return markup

def markup_what_u_got(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Рубли/RUB", callback_data = "HAS_RUB___" + str(chatId)),
        InlineKeyboardButton("Лиры/TRL", callback_data = "HAS_TRL___" + str(chatId))
    )
    return markup

def markup_need_val(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Понятно", callback_data = "PON___" + str(chatId)),
    )
    return markup

@bot.message_handler(commands = ['Start',"start"])
def start(message):
    insert_new_user(db_conn,"USER_DATA",message.chat.id,message.chat.username)
    bot.send_message(message.chat.id, "Найти обмен - бот для поиска \
        контр-агента по обмену денег \n\
        Контр-агент - такой же человек, которому нужно перевести или обменять деньги, \
        но связан ограничениями, лиюо невыгодным локальным курсом.\n\
        Бот не является гарантом: безопасность вас и ваших средств лежит на вас. \n\
        Чтобы оставить заявку введите:\n /обмен\n... \n\n\
        ", )

@bot.message_handler(commands = ['обмен'])
def obmen(message):
    update_db_value(db_conn,"USER_DATA",message.chat.id,"MENU_POS",1)
    insert_new_temp_bid(db_conn,"TEMP_BID_DATA",message.chat.id)
    msg =  "Желаемая валюта после обмена:" #"Выберите валюту для получения:"  "Какая валюта тебе нужна?" 
    bot.send_message(message.chat.id, msg, reply_markup = markup_need_currency(message.chat.id))

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    print(call.data)
    if call.data.split("_")[0] == "GET":
        print(f'Юзеру {call.data.split("___")[1]} нужны {call.data.split("_")[1]}')
        update_db_value(db_conn,"USER_DATA",call.data.split("___")[1],"MENU_POS",2)
        update_db_value(db_conn,"TEMP_BID_DATA",call.data.split("___")[1],"NEED_CUR",call.data.split("_")[1])
        msg = "Способ передачи средств Вам" #"Как хочешь получить деньги?"
        bot.send_message(int(call.data.split("___")[1]), msg, reply_markup = markup_receive(call.data.split("___")[1]))
    elif call.data.split("_")[0] == "REC":
        print(f'Юзер {call.data.split("___")[1]} хочет получить их в/на {call.data.split("_")[1]}')
        update_db_value(db_conn,"USER_DATA",call.data.split("___")[1],"MENU_POS",3)
        update_db_value(db_conn,"TEMP_BID_DATA",call.data.split("___")[1],"NEED_LOC",call.data.split("_")[1])
        msg = "Ваша валюта для обмена:" #"Какая у тебя валюта?"
        bot.send_message(int(call.data.split("___")[1]), msg, reply_markup = markup_what_u_got(call.data.split("___")[1]))
    elif call.data.split("_")[0] == "HAS":
        print(f'У Юзера {call.data.split("___")[1]} есть {call.data.split("_")[1]}')
        update_db_value(db_conn,"USER_DATA",call.data.split("___")[1],"MENU_POS",4)
        update_db_value(db_conn,"TEMP_BID_DATA",call.data.split("___")[1],"HAS_CUR",call.data.split("_")[1])
        msg = "Способ передачи средств Вами:"#"Как можешь средства передать?"
        bot.send_message(int(call.data.split("___")[1]), msg, reply_markup = markup_how_u_send(call.data.split("___")[1]))
    elif call.data.split("_")[0] == "FROM":
        print(f'У Юзера {call.data.split("___")[1]} есть {call.data.split("_")[1]}')
        update_db_value(db_conn,"USER_DATA",call.data.split("___")[1],"MENU_POS",5)
        update_db_value(db_conn,"TEMP_BID_DATA",call.data.split("___")[1],"HAS_LOC",call.data.split("_")[1])
        msg = f'Введите необходимую сумму "валюта" для получения:\nВведите 0 для пропуска шага' #'сколько нужно'
        bot.send_message(int(call.data.split("___")[1]), msg)
    elif call.data.split("_")[0] == "PON":
        print(f'У Юзера {call.data.split("___")[1]} есть {call.data.split("_")[1]}')
        msg = "Введите сумму средств для обмена:" #"Дальше нужно будет ввести сколько хотите получить в валюте получения и/или сколько хотите обменять в вашей"
        bot.send_message(int(call.data.split("___")[1]), msg)
bot.polling()


@bot.message_handler(func=lambda message: True)
def command_text_hi(message):
    if get_val_db(db_conn,"USER_DATA",message.chat.id,"MENU_POS") == 5:
        if "".join(message.text.split()).isdigit():
            update_db_value(db_conn,"USER_DATA",message.chat.id,"MENU_POS",6)
            update_db_value(db_conn,"TEMP_BID_DATA",message.chat.id,"NEED_VAL",int("".join(message.text.split())))
            msg = "Введите сумму средств для обмена:"
            bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, "Введите целое число, например 123456")
    elif get_val_db(db_conn,"USER_DATA",message.chat.id,"MENU_POS") == 6:
        if "".join(message.text.split()).isdigit():
            update_db_value(db_conn,"USER_DATA",message.chat.id,"MENU_POS",7)
            update_db_value(db_conn,"TEMP_BID_DATA",message.chat.id,"NEED_VAL",int("".join(message.text.split())))
            msg = "Пока все:"
            bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, "Введите целое число, например 123456")