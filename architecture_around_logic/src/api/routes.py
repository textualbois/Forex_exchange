from architecture_around_logic.src.bids.new_bid import controller as new_bid
from architecture_around_logic.config.user_states import *
from state_machine import get_state


def route_callback(route, user_input, secondary_input, user_id, message_id):
	if markup_identity == "MAINMENU":
		ur.reply_to_mainmenu(user_id)
	elif markup_identity == create_new_bid:  # 0
		new_bid.handle_newbid_request(user_id)
		ur.reply_to_newbid(user_id, forex_db)
	elif markup_identity == "GET":  # 1
		ur.reply_to_get(markup_result, user_id)  # goes to rec
	elif markup_identity == "REC":  # 2
		ur.reply_to_rec(markup_result, user_id)  # goes to has
	elif markup_identity == "HAS":  # 3
		ur.reply_to_has(markup_result, user_id)  # goes to from
	elif markup_identity == "FROM":  # 4
		ur.reply_to_from(markup_result, user_id)  # goes to status check (has_val)
	elif markup_identity == "CHECK":  # 9
		ur.reply_to_check(markup_result, user_id, forex_db)
	elif markup_identity == "MYBIDS":  # B1
		ur.reply_to_mybids(user_id)  # ask which of his bids user wants to view (WHATBIDS)
	elif markup_identity == "WHATBIDS":  # B2
		ur.reply_to_whatbids(markup_result, user_id, forex_db)  #
	elif markup_identity == "MYACTIVEBIDS":  # B3.a
		ur.show_my_active_bids(user_id, forex_db)
	# elif markup_identity == "MYFULFILLEDBIDS":  # B3.b
	#     ur.reply_to_myfulfilledbids(markup_result, user_id, forex_db)
	elif markup_identity == "MYCANCELLEDBIDS":  # B3.c
		ur.show_my_cancelled_bids(user_id, forex_db)

	elif markup_identity == "DELETEBID":
		ur.request_to_remove_bid(markup_result, user_id, forex_db)

	elif markup_identity == "MATCHTHISBID":
		matching_bids.ask_range(markup_result, user_id, forex_db)

	# elif markup_identity == "OTHERSBIDS":
	#    ur.reply_to_otherbids(markup_result, user_id, forex_db)
	# elif markup_identity == "OTHERSBIDSNEEDCUR":
	#    ur.reply_to_othersbis(markup_result, user_id, forex_db)
	# elif markup_identity == "OTHERSBIDSHASCUR":
	#    ur.reply_to_othersbis(markup_result, user_id, forex_db)
	# elif markup_identity == "OTHERSBIDSNEEDLOC":
	#    ur.reply_to_othersbis(markup_result, user_id, forex_db)
	# elif markup_identity == "OTHERSBIDSNEEDHAS":
	#    ur.reply_to_othersbis(markup_result, user_id, forex_db)

	elif markup_identity == "SEARCHRANGE":
		matching_bids.setup_matching_bids(int(markup_result), user_id, forex_db)
	elif markup_identity == "MYBIDMATCHES":
		matching_bids.show_matches(user_id, forex_db)

	elif markup_identity == "SENDEXCHANGEREQUEST":
		outgoing_exchange_requests.send_exchange_request(markup_result, user_id, forex_db)
	elif markup_identity == "REPLYTOREQUEST":
		outgoing_exchange_requests.manage_askers_reply(markup_result, markup_result2, user_id, forex_db)
	# elif markup_identity == "MAKINGOFFER":
	#     outgoing_exchange_requests.send_request(markup_result, user_id, forex_db)

	# elif markup_identity == "OTHERSBIDS":
	#    ur.reply_to_otherbids(markup_result, user_id, forex_db)
	# elif markup_identity == "FEEDBACK":
	#    ur.reply_to_feedback(markup_result, user_id)
	elif markup_identity == "CONTACTSMENU":
		bot.send_message(int(user_id), "Меню контактов", btmrkp.markup_my_contacts(user_id))
	elif markup_identity == "VIEWCONTACTS":
		contacts.view_my_contacts(user_id, forex_db)
	elif markup_identity == "ADDCONTACTS":
		contacts.ask_for_contacts_in_menu(user_id)


def route_message(route, user_input, user_id, message_id):
	state = get_state(user_id)