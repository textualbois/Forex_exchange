from logic import *
from check_input import *
from architecture_around_logic.src.api import state_machine as sm
from architecture_around_logic.src import helpers
from architecture_around_logic.config import *


def handle_newbid_request(user_id):
	choose_wanted_currency(user_id)


def handle_required_currency(user_id, input_val):
	store_wanted_currency(user_id, input_val)
	choose_how_to_receive_currency(user_id)


def handle_wanted_reception_method(user_id, input_val):
	store_how_to_receive_currency(user_id, input_val)
	what_currency_user_has(user_id)


def handle_available_currency(user_id, input_val):
	store_what_currency_user_has(user_id, input_val)
	where_is_users_currency(user_id)


def handle_users_currency_location(user_id, input_val):
	store_where_user_has_currency(user_id, input_val)
	how_much_user_has(user_id)


def handle_available_currency_amount(user_id, input_val):
	if amount_is_valid(input_val):
		store_how_much_user_has(user_id, input_val)
		sm.switch_state(user_id, user_entered_available_amount)
		how_much_user_wants(user_id)
	else:
		how_much_user_has_2(user_id)


def handle_required_currency_amount(user_id, input_val):
	if amount_is_valid(input_val):
		store_how_much_user_wants(user_id, input_val)
		sm.switch_state(user_id, user_entered_required_amount)
		ask_user_location(user_id)
	else:
		how_much_user_wants_2(user_id)


def handle_users_location(user_id, input_val):
	location = parse_coordinates(input_val)
	if location_is_valid(location):
		store_coordinates(user_id, location)
		sm.switch_state(user_id, user_entered_location_coordinates)
		ask_location_alias(user_id)


def handle_location_alias(user_id, input_val):
	# todo add sql safety filter
	# actually sql has a built-in safety filter
	# maybe just add length of input_val filter
	store_location_alias(user_id, input_val)
	sm.switch_state(user_id, user_entered_location_alias)
	ask_user_to_check_input(user_id)


def handle_input_check(user_id, input_val):
	if input_val == "OK":
		check_result_ok(user_id)
		transfer_to_main_db(user_id)
		sm.clear_state(user_id)
	elif input_val == "USERBAD":
		check_result_userbad(user_id)
		choose_wanted_currency(user_id)
	elif input_val == "BOTBAD":
		check_result_botbad(user_id)
