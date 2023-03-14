import strings as s
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_menu(lang):
	markup = InlineKeyboardMarkup()
	markup.width = 1
	for key, value in s.contacts_menu_buttons(lang).items():
		markup.add(
			InlineKeyboardButton(value, callback_data=f"{key}__")
		)
	return markup
