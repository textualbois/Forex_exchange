import strings as s
import redis_db as rf_glob
from architecture_around_logic.src.helpers.string_formatting import *

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


def check_input(lang, bid_data):
	msg_dict = s.check_input(lang)
	NEED_VAL = int(bid_data["NEED_VAL"])
	HAS_VAL = int(bid_data["HAS_VAL"])
	NEED_CUR = bid_data["NEED_CUR"]
	HAS_CUR = bid_data["HAS_CUR"]
	NEED_LOC = bid_data["NEED_LOC"]
	HAS_LOC = bid_data["HAS_LOC"]
	LOC_MAIN_ALIAS = bid_data["LOC_MAIN_ALIAS"]
	msg = (f"{msg_dict['your_location_is']}{LOC_MAIN_ALIAS}\n"
		   f"{msg_dict['you_have']}{HAS_VAL:,}{msg_dict['in']}{format_currency_name(HAS_CUR, lang)} "
		   f"{format_currency_location(HAS_LOC, lang)}\n"
		   f"{msg_dict['you_need']} {NEED_VAL:,}{msg_dict['in']}{format_currency_name(NEED_CUR, lang)} "
		   f"{format_currency_location(NEED_LOC, lang)}\n"
		   f"{msg_dict['approximate_rate']}"
		   f"{HAS_CUR + '/' + NEED_CUR if HAS_VAL >= NEED_VAL else NEED_CUR + '/' + HAS_CUR}:\n"
		   f"{max(NEED_VAL / HAS_VAL, HAS_VAL / NEED_VAL):.4}\n"
		   f"{msg_dict['inverse_rate']}"
		   f"{HAS_CUR + '/' + NEED_CUR if NEED_VAL < NEED_VAL else NEED_CUR + '/' + HAS_CUR}:\n"
		   f"{min(HAS_VAL / NEED_VAL, NEED_VAL / HAS_VAL):.4}\n")
	return msg


# todo saving_bid
def saving_bid(lang):
	msg_dict = s.saving_bid(lang)
	msg = msg_dict['msg_start']
	return msg


# todo msg = "Попробуем ещё раз.\n Какую валюту хотите получить:"
def retry_newbid(lang):
	msg_dict = s.retry_newbid(lang)
	msg = msg_dict['msg_start']
	return msg


# todo ask feedback
def ask_feedback(lang):
	msg_dict = s.ask_feedback(lang)
	msg = msg_dict['msg_start']
	return msg