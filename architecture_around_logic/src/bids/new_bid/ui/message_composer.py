import strings as s
import redis_db as rf_glob


def choose_needed_currency(lang):
	msg_dict = s.choose_wanted_currency(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg


def choose_how_to_receive_currency(lang):
	msg_dict = s.choose_how_to_receive_currency(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg


def what_currency_do_you_have(lang):
	msg_dict = s.what_currency_do_you_have(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg


def how_can_you_send_currency(lang):
	msg_dict = s.how_can_you_send_money(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg


def how_much_you_have(lang, user_id):
	msg_dict = s.how_much_you_have(lang)
	msg = f"{msg_dict['msg_start']}{rf_glob.read_hash(user_id, 'HAS_CUR')}{msg_dict['msg_end']}"
	return msg


def how_much_you_have_2(lang):
	msg_dict = s.enter_valid_value(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg


def how_much_you_want(lang, user_id):
	msg_dict = s.how_much_you_want(lang)
	msg = f"{msg_dict['msg_start']}{rf_glob.read_hash(user_id, 'NEED_CUR')}{msg_dict['msg_end']}"
	return msg


def how_much_you_want_2(lang):
	msg_dict = s.enter_valid_value(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg


def what_is_your_location(lang):
	msg_dict = s.what_is_your_location(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg


def location_alias(lang):
	msg_dict = s.location_alias(lang)
	msg = f"{msg_dict['msg_start']}"
	return msg