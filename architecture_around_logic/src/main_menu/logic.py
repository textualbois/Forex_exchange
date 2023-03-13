from ui import *
from architecture_around_logic.src.connections import bot
from architecture_around_logic.config.language_alias import *


def show_menu(user_id, lang=rus):
	bot.send_message(user_id. mc.main_menu(lang), reply_markup=markups.show_menu(lang))
