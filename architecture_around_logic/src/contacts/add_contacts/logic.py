from ui import *
from ....src.connections import bot
from ....config.language_alias import *
from ....config.db_aliases import col_viber_number, col_local_number, col_whatsapp_number, col_telegram_number
from ...main_db import update_contact_number as store_number

# todo add single function that takes column name instead of 4 storing functions


def send_instructions(user_id, lang=rus):
	bot.send_message(user_id, mc.send_instructions(lang))


def tell_user_input_is_bad(user_id, lang=rus):
	bot.send_message(user_id, mc.your_input_is_bad(lang))


def ask_for_whatsapp(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_whatsapp(lang))


def store_whatsapp(user_id, input_val):
	store_number(col_whatsapp_number, user_id, input_val)


def ask_for_telegram(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_telegram(lang))


def store_telegram(user_id, input_val):
	store_number(col_telegram_number, user_id, input_val)


def ask_for_viber(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_viber(lang))


def store_viber(user_id, input_val):
	store_number(col_viber_number, user_id, input_val)


def ask_for_local_number(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_local_number(lang))


def store_local_number(user_id, input_val):
	store_number(col_local_number, user_id, input_val)


def end_add_contacts_interaction(user_id, lang=rus):
	bot.send_message(user_id, mc.saved_your_contacts(lang))



