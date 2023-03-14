from architecture_around_logic.config.user_states import view_contacts, add_contacts
from architecture_around_logic.config.language_alias import *

contacts_menu_buttons_ru = {view_contacts: "Посмотреть мои данные",
							add_contacts: "Добавить свои данные"}

contacts_menu_buttons_eng = {view_contacts: "View my data",
							 add_contacts: "Enter my contacts"}

contacts_menu_buttons = {rus: contacts_menu_buttons_ru, eng: contacts_menu_buttons_eng}

contacts_menu_ru = {"msg_start": "Меню контактов"}
contacts_menu_eng = {"msg_start": "Contacts menu"}

contacts_menu = {rus: contacts_menu_ru, eng: contacts_menu_eng}