from ui import *
from architecture_around_logic.src.connections import bot
from architecture_around_logic.config.language_alias import *

import redis_db as rf_glob


"""
Entry point for a new bid.
choose_wanted_currency asks what currency user wants
"""
def choose_wanted_currency(user_id):
	bot.send_message(int(user_id), mc.choose_needed_currency(rus), reply_markup=markups.needed_currency())

def store_wanted_currency(user_id):
	rf_glob.update_hash(user_id, "NEED_CUR", )

def choose_how_to_receive_currency(user_id):
	store_wanted_currency
	bot.send_message(int(user_id), mc.choose_how_to_receive_currency(rus),
					 reply_markup=markups.how_to_receive_currency())


def store_how_to_receive_currency():
	pass


def where_is_users_currency():
	pass


def store_where_user_has_currency():
	pass


def what_currency_user_has():
	pass


def store_what_currency_user_has():
	pass

def how_much_user_has():
	pass

def store_how_much_user_has():
	pass

def how_much_user_wants():
	pass

def store_how_much_user_wants():
	pass

def ask_user_location():


def handle_users_location_reply():

	if location_is_valid(location):
		rf_global.update_hash(user_id, main_location_latitude, location[0], entered_valid_location)
		rf_global.update_hash(user_id, main_location_longitude, location[1], entered_valid_location)
		bot.send_message(user_id, mc.location_alias, )

def store_user_location():
	pass