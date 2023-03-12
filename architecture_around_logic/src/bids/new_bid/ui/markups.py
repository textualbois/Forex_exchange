from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import strings as s
from architecture_around_logic.config import user_states as us


def needed_currency(lang):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    for key, value in s.wanted_currency_buttons(lang).items():
        markup.add(
            InlineKeyboardButton(value, callback_data=f"{us.user_entered_what_currency_he_wants}_{key}__")
        )
    return markup


def how_to_receive_currency(lang):
    markup = InlineKeyboardMarkup()
    markup.width = 1
    for key, value in s.how_to_receive_currency_buttons(lang).items():
        markup.add(
            InlineKeyboardButton(value, callback_data=f"{us.user_entered_where_he_wants_the_currency}_{key}__")
        )
    return markup


def where_is_users_currency(lang):
    markup = InlineKeyboardMarkup()
    markup.width = 1
    for key, value in s.how_can_you_send_currency_buttons(lang).items():
        markup.add(
            InlineKeyboardButton(value, callback_data=f"{us.user_entered_where_he_has_currency}_{key}__")
        )
    return markup


def what_currency_has_user_got(lang):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    for key, value in s.available_currency_buttons(lang).items():
        markup.add(
            InlineKeyboardButton(value, callback_data=f"{us.user_entered_what_currency_he_has}_{key}__")
        )
    return markup


def check_input(lang):
    markup = InlineKeyboardMarkup()
    markup.width = 1
    for key, value in s.check_input(lang).items():
        markup.add(
            InlineKeyboardButton(value, callback_data=f"{us.user_checked_newbid_input}_{key}__")
        )
    return markup
