from ui import *
from architecture_around_logic.src.connections import bot
from architecture_around_logic.config.language_alias import *
from architecture_around_logic.config.user_states import *


import redis_db as rf_glob


"""
Entry point for a new bid.
choose_wanted_currency asks what currency user wants
"""
def choose_wanted_currency(user_id, lang=rus):
	bot.send_message(int(user_id), mc.choose_needed_currency(lang),
					 reply_markup=markups.needed_currency(lang))

def store_wanted_currency(user_id, input_val):
	rf_glob.update_hash(user_id, "NEED_CUR", input_val)

def choose_how_to_receive_currency(user_id, lang=rus):
	bot.send_message(int(user_id), mc.choose_how_to_receive_currency(lang),
					 reply_markup=markups.how_to_receive_currency(lang))

def store_how_to_receive_currency(user_id, input_val):
	rf_glob.update_hash(user_id, "NEED_LOC", input_val)


def where_is_users_currency(user_id, lang=rus):
	bot.send_message(user_id, mc.how_can_you_send_currency(lang),
					 reply_markup=markups.where_is_users_currency(lang))


def store_where_user_has_currency(user_id, input_val):
	rf_glob.update_hash(user_id, "HAS_LOC", input_val)


def what_currency_user_has(user_id, lang=rus):
	bot.send_message(user_id, mc.what_currency_do_you_have(lang),
					 reply_markup=markups.what_currency_has_user_got(lang))


def store_what_currency_user_has(user_id, input_val):
	rf_glob.update_hash(user_id, "HAS_CUR", input_val)


def how_much_user_has(user_id, lang=rus):
	bot.send_message(user_id, mc.how_much_you_have(lang, user_id))

def how_much_user_has_2(user_id, lang=rus):
	bot.send_message(user_id, mc.how_much_you_have_2(lang))

def store_how_much_user_has(user_id, input_val):
	rf_glob.update_hash(user_id, "HAS_VAL", input_val)


def how_much_user_wants(user_id, lang=rus):
	bot.send_message(user_id, mc.how_much_you_want(lang, user_id))


def store_how_much_user_wants(user_id, input_val):
	rf_glob.update_hash(user_id, "NEED_VAL", input_val)


def ask_user_location(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_location(lang))


def parse_coordinates(input_val):
	return (re.sub(r"[\r\n\s\(\)]+", "", input_val)).split(",")


def store_coordinates(user_id, location):
	rf_glob.update_hash(user_id, main_location_latitude, location[0])
	rf_glob.update_hash(user_id, main_location_longitude, location[1])


def ask_location_alias(user_id, lang=rus):
	bot.send_message(user_id, mc.location_alias(lang))