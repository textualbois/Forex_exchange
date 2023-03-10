from logic import *
from check_input import *
from architecture_around_logic.src.api import state_machine as sm

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
		sm.switch_state(user_id, entered_available_currency)
		how_much_user_wants(user_id)
	else:
		how_much_user_has_2(user_id)


def handle_required_currency_amount(user_id, input_val):
	if amount_is_valid(input_val):
	pass


def handle_users_location(user_id, input_val):
	location = parse_coordinates(input_val)
	if location_is_valid(location):
		store_coordinates()


def handle_location_alias(user_id, input_Val):
	pass


def handle_input_check(user_id):
	pass