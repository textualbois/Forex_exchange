from architecture_around_logic.src.api import state_machine as sm
from architecture_around_logic.config import *
from architecture_around_logic.src.contacts.contacts_helpers import *
from logic import *


def handle_add_contacts(user_id):
	sm.switch_state(user_id, user_wants_to_add_contacts)
	send_instructions(user_id)
	ask_for_whatsapp(user_id)


def handle_whatsapp_number(user_id, user_input):
	clean_number = format_number(user_input)
	if clean_number != '+0':
		if check_input_good(clean_number):
			sm.switch_state(user_id, user_entered_whatsapp)
			ask_for_telegram(user_id)
			store_whatsapp(user_id, clean_number)
		else:
			tell_user_input_is_bad(user_id)
			send_instructions(user_id)
			ask_for_whatsapp(user_id)
	else:
		sm.switch_state(user_id, user_entered_whatsapp)
		ask_for_telegram(user_id)


def handle_telegram_number(user_id, user_input):
	clean_number = format_number(user_input)
	if clean_number != '+0':
		if check_input_good(clean_number):
			sm.switch_state(user_id, user_entered_telegram)
			ask_for_viber(user_id)
			store_telegram(user_id, clean_number)
		else:
			tell_user_input_is_bad(user_id)
			send_instructions(user_id)
			ask_for_telegram(user_id)
	else:
		sm.switch_state(user_id, user_entered_telegram)
		ask_for_viber(user_id)


def handle_viber_number(user_id, user_input):
	clean_number = format_number(user_input)
	if clean_number != '+0':
		if check_input_good(clean_number):
			sm.switch_state(user_id, user_entered_viber)
			ask_for_local_number(user_id)
			store_viber(user_id, clean_number)
		else:
			tell_user_input_is_bad(user_id)
			send_instructions(user_id)
			ask_for_viber(user_id)
	else:
		sm.switch_state(user_id, user_entered_telegram)
		ask_for_local_number(user_id)


def handle_local_number(user_id, user_input):
	clean_number = format_number(user_input)
	if clean_number != '+0':
		if check_input_good(clean_number):
			sm.switch_state(user_id, user_entered_local_number)
			ask_for_local_number(user_id)
			store_local_number(user_id, clean_number)
		else:
			tell_user_input_is_bad(user_id)
			send_instructions(user_id)
			end_add_contacts_interaction(user_id)
	else:
		sm.switch_state(user_id, user_entered_local_number)
		end_add_contacts_interaction(user_id)




