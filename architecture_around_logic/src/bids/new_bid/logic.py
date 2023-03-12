from ui import *
from architecture_around_logic.src.connections import bot
from architecture_around_logic.config.language_alias import *
from architecture_around_logic.config.user_states import *
from architecture_around_logic.config import db_aliases as db_alias
import re
import redis_db as rf_glob



"""
Entry point for a new bid.
choose_wanted_currency asks what currency user wants
"""
def choose_wanted_currency(user_id, lang=rus):
	bot.send_message(int(user_id), mc.choose_needed_currency(lang),
					 reply_markup=markups.needed_currency(lang))

def store_wanted_currency(user_id, input_val):
	rf_glob.update_hash(user_id, db_alias.needed_currency, input_val)

def choose_how_to_receive_currency(user_id, lang=rus):
	bot.send_message(int(user_id), mc.choose_how_to_receive_currency(lang),
					 reply_markup=markups.how_to_receive_currency(lang))

def store_how_to_receive_currency(user_id, input_val):
	rf_glob.update_hash(user_id, db_alias.user_needs_money_here, input_val)


def where_is_users_currency(user_id, lang=rus):
	bot.send_message(user_id, mc.how_can_you_send_currency(lang),
					 reply_markup=markups.where_is_users_currency(lang))


def store_where_user_has_currency(user_id, input_val):
	rf_glob.update_hash(user_id, db_alias.users_bank_residency, input_val)


def what_currency_user_has(user_id, lang=rus):
	bot.send_message(user_id, mc.what_currency_do_you_have(lang),
					 reply_markup=markups.what_currency_has_user_got(lang))


def store_what_currency_user_has(user_id, input_val):
	rf_glob.update_hash(user_id, db_alias.available_currency, input_val)


def how_much_user_has(user_id, lang=rus):
	bot.send_message(user_id, mc.how_much_you_have(lang, user_id))


def how_much_user_has_2(user_id, lang=rus):
	bot.send_message(user_id, mc.how_much_you_have_2(lang))


def store_how_much_user_has(user_id, input_val):
	rf_glob.update_hash(user_id, db_alias.available_amount, input_val)


def how_much_user_wants(user_id, lang=rus):
	bot.send_message(user_id, mc.how_much_you_want(lang, user_id))


def how_much_user_wants_2(user_id, lang=rus):
	bot.send_message(user_id, mc.how_much_you_want_2(lang))


def store_how_much_user_wants(user_id, input_val):
	rf_glob.update_hash(user_id, db_alias.amount_needed, input_val)


def ask_user_location(user_id, lang=rus):
	bot.send_message(user_id, mc.what_is_your_location(lang))


# todo move to global helpers or local helpers (input parser)
def parse_coordinates(input_val):
	return (re.sub(r"[\r\n\s\(\)]+", "", input_val)).split(",")


def store_coordinates(user_id, location):
	rf_glob.update_hash(user_id, db_alias.main_location_latitude, location[0])
	rf_glob.update_hash(user_id, db_alias.main_location_longitude, location[1])


def ask_location_alias(user_id, lang=rus):
	bot.send_message(user_id, mc.location_alias(lang))


def store_location_alias(user_id, location_alias):
	rf_glob.update_hash(user_id, db_alias.main_location_alias, location_alias)


def ask_user_to_check_input(user_id, lang=rus):
	newbid_data = rf_local.get_newbid_data(user_id)
	bot.send_message(user_id, mc.check_input(lang, newbid_data),
					 reply_markup=markups.check_input(lang))


def check_result_ok(user_id, lang=rus):
	bot.send_message(user_id, mc.saving_data(lang))
	main_menu.go_to_main_menu(user_id)


def transfer_to_main_db(user_id):
	newbid_data = rf_local.get_newbid_data(user_id)
	db.store_newbid(user_id, newbid_data)

def check_result_userbad(user_id):
	# todo msg = "Попробуем ещё раз.\n Какую валюту хотите получить:"
	pass


def check_result_botbad(user_id):
	#  todo feedback option
	pass


