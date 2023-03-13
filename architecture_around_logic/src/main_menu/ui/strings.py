from architecture_around_logic.config.user_states import create_new_bid, \
	go_to_mybids_menu, go_to_others_bids, go_to_contacts_menu, go_to_incoming_bids, feedback_menu
from architecture_around_logic.config.language_alias import *

main_menu_buttons_ru = {create_new_bid: "Оставить заявку",
						go_to_mybids_menu: "Посмотреть свои заявки",
						go_to_incoming_bids: "Входящие запросы",
						go_to_others_bids: "Посмотреть подходящие обмены",
						go_to_contacts_menu: "Мои данные",
						feedback_menu: "Обратная связь. Ошибки в боте"}

main_menu_buttons_eng = {create_new_bid: "Place bid",
						go_to_mybids_menu: "My bids",
						go_to_incoming_bids: "Incoming offers",
						go_to_others_bids: "Find bids",
						go_to_contacts_menu: "Мy data",
						feedback_menu: "Feedback"}

main_menu_buttons = {rus: main_menu_buttons_ru, eng: main_menu_buttons_eng}

main_menu_ru = {"msg_start": "Основное меню"}
main_menu_eng = {"msg_start": "Main menu"}

main_menu = {rus: main_menu_ru, eng: main_menu_eng}


