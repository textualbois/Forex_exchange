from architecture_around_logic.src.bids.new_bid import controller as new_bid
from architecture_around_logic.src.main_menu import logic as main_menu
from architecture_around_logic.src.contacts.contacts_menu import logic as contacts_menu
from architecture_around_logic.config.user_states import *
from state_machine import get_state


def route_callback(route, user_input, secondary_input, user_id, message_id):
	if route == go_to_main_menu:
		main_menu.show_menu(user_id)
	elif route == create_new_bid:  # 0
		new_bid.handle_newbid_request(user_id)
	elif route == user_entered_what_currency_he_wants:  # 1
		new_bid.handle_required_currency(user_id, user_input)
	elif route == user_entered_where_he_wants_the_currency:  # 2
		new_bid.handle_users_currency_location(user_id, user_input)
	elif route == user_entered_what_currency_he_has:  # 3
		new_bid.handle_available_currency(user_id, user_input)
	elif route == user_entered_where_he_has_currency:
		new_bid.handle_users_currency_location(user_id, user_input)# 4
	elif route == user_checked_newbid_input:
		new_bid.handle_input_check(user_id, user_input)# 9

	elif route == "MYBIDS":  # B1
		ur.reply_to_mybids(user_id)  # ask which of his bids user wants to view (WHATBIDS)
	elif route == "WHATBIDS":  # B2
		ur.reply_to_whatbids(user_input, user_id, forex_db)  #
	elif route == "MYACTIVEBIDS":  # B3.a
		ur.show_my_active_bids(user_id, forex_db)
	# elif route == "MYFULFILLEDBIDS":  # B3.b
	#     ur.reply_to_myfulfilledbids(user_input, user_id, forex_db)
	elif route == "MYCANCELLEDBIDS":  # B3.c
		ur.show_my_cancelled_bids(user_id, forex_db)

	elif route == "DELETEBID":
		ur.request_to_remove_bid(user_input, user_id, forex_db)

	elif route == "MATCHTHISBID":
		matching_bids.ask_range(user_input, user_id, forex_db)

	# elif route == "OTHERSBIDS":
	#    ur.reply_to_otherbids(user_input, user_id, forex_db)
	# elif route == "OTHERSBIDSNEEDCUR":
	#    ur.reply_to_othersbis(user_input, user_id, forex_db)
	# elif route == "OTHERSBIDSHASCUR":
	#    ur.reply_to_othersbis(user_input, user_id, forex_db)
	# elif route == "OTHERSBIDSNEEDLOC":
	#    ur.reply_to_othersbis(user_input, user_id, forex_db)
	# elif route == "OTHERSBIDSNEEDHAS":
	#    ur.reply_to_othersbis(user_input, user_id, forex_db)

	elif route == "SEARCHRANGE":
		matching_bids.setup_matching_bids(int(user_input), user_id, forex_db)
	elif route == "MYBIDMATCHES":
		matching_bids.show_matches(user_id, forex_db)

	elif route == "SENDEXCHANGEREQUEST":
		outgoing_exchange_requests.send_exchange_request(user_input, user_id, forex_db)
	elif route == "REPLYTOREQUEST":
		outgoing_exchange_requests.manage_askers_reply(user_input, user_input2, user_id, forex_db)
	# elif route == "MAKINGOFFER":
	#     outgoing_exchange_requests.send_request(user_input, user_id, forex_db)

	# elif route == "OTHERSBIDS":
	#    ur.reply_to_otherbids(user_input, user_id, forex_db)
	# elif route == "FEEDBACK":
	#    ur.reply_to_feedback(user_input, user_id)
	elif route == go_to_contacts_menu:
		contacts_menu.show_menu(user_id)
	elif route == "VIEWCONTACTS":
		contacts.view_my_contacts(user_id, forex_db)
	elif route == "ADDCONTACTS":
		contacts.ask_for_contacts_in_menu(user_id)


def route_message(route, user_input, user_id, message_id):
	state = get_state(user_id)
	if state < user_making_newbid:
		if state == user_entered_available_amount:  # 5
			new_bid.handle_available_currency_amount(user_id, user_input)
			ur.reply_to_has_val(message, user_id)  # goes to state check (need_val)
		elif state == user_entered_required_amount:  # 6
			new_bid.handle_required_currency_amount(user_id, user_input)
			ur.reply_to_need_val(message, user_id)  # goes to state check (main loc coordinates)
		elif state == user_entered_location_coordinates:  # 7:
			new_bid.handle_users_location(user_id, user_input)
			ur.reply_to_main_loc_coordinates(message, user_id)  # goes to state check (main loc alias)
		elif state == user_entered_location_alias:  # 8:
			new_bid.handle_location_alias(user_id, user_input)
			ur.reply_to_main_loc_alias(message, user_id)
	elif state < 20:
		if state == 10:
			contacts.store_whatsapp_number(message, user_id, forex_db)
		elif state == 11:
			contacts.store_telegram_number(message, user_id, forex_db)
		elif state == 12:
			contacts.store_viber_number(message, user_id, forex_db)
		elif state == 13:
			contacts.store_local_number_from_menu(message, user_id, forex_db)
	elif state < 30:
		if state == 20:
			contacts.store_whatsapp_number(message, user_id, forex_db)
		elif state == 21:
			contacts.store_telegram_number(message, user_id, forex_db)
		elif state == 22:
			contacts.store_viber_number(message, user_id, forex_db)
		elif state == 23:
			contacts.store_local_number_in_exchange_request(message, user_id, forex_db)