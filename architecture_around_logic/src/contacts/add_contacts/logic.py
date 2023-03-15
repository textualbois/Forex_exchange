from ui import *
from architecture_around_logic.src.connections import bot
from architecture_around_logic.config.language_alias import *
from architecture_around_logic.config import db_aliases as db_alias

# todo add single function that takes column name instead of 4 storing functions


def send_instructions(user_id, lang=rus):
	bot.send_message(user_id, mc.send_instructions(lang))


def tell_user_input_is_bad(user_id, lang=rus):
	bot.send_message(user_id, mc.your_input_is_bad(lang))


def ask_for_whatsapp(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_whatsapp(lang))


def store_whatsapp(user_id, input_val):
	db_global.update_db_value(db_alias.table_user_data, db_alias.col_whatsapp_number, user_id, input_val)


def ask_for_telegram(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_telegram(lang))


def store_telegram(user_id, input_val):
	db_global.update_db_value(db_alias.table_user_data, db_alias.col_telegram_number, user_id, input_val)


def ask_for_viber(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_viber(lang))


def store_viber(user_id, input_val):
	db_global.update_db_value(db_alias.table_user_data, db_alias.col_viber_number, user_id, input_val)


def ask_for_local_number(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_local_number(lang))


def store_local_number(user_id, input_val):
	db_global.update_db_value(db_alias.table_user_data, db_alias.col_local_number, user_id, input_val)


def end_add_contacts_interaction(user_id, lang=rus):
	bot.send_message(user_id, mc.saved_your_contacts(lang))



