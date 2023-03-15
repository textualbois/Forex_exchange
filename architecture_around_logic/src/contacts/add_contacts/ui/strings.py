from architecture_around_logic.config.language_alias import *

send_instructions_ru = {'msg_start': ("Необходимо заполнить контактные данные для отправки их пользователям. "
									  "Нужен хотя бы один из видов связи:\n"
									  "whatsapp, telegram, viber или местный номер.\n"
									  "Указывайте номер с международным кодом а не внутренним.\n"
									  "Например +7 999 999 99 99 а не 8 999 999 99 99 для России\n"
									  "Мы не передаем ваши контакты другому пользователю, "
									  "предварительно не спросив вас "
									  "и не уточнив актуальность конкретной вашей заявки.")}
send_instructions_eng = {'msg_start': ("Fill out the contact data, so that your bids are visible to other users. "
									   "We need at least one way to reach you:\n"
									   "whatsapp, telegram, viber or local number.\n"
									   "Enter the number with it's international code.\n"
									   "i.e +44 7999 999999, not 07999 999999 for U.K. numbers\n"
									   "We do not share your data with other users without asking you beforehand "
									   "and making sure that your bid is still relevant.")}

send_instructions = {rus: send_instructions_ru, eng: send_instructions_eng}

input_is_bad_ru = {'msg_start': ("Мы не распознали номер, попробуйте снова, "
								 "или дайте обратную связь, через основное меню")}
input_is_bad_eng = {'msg_start': ("We couldn't recognise the number, please try again "
								  "or leave us feedback through the main menu")}
input_is_bad = {rus: input_is_bad_ru, eng: input_is_bad_eng}


ask_for_whatsapp_ru = {'msg_start': "Укажите номер используемый в Whatsapp. Для пропуска укажите 0"}
ask_for_whatsapp_eng = {'msg_start': "Enter your Whatsapp number. To skip enter 0"}
ask_for_whatsapp = {rus: ask_for_whatsapp_ru, eng: ask_for_whatsapp_eng}

ask_for_telegram_ru = {'msg_start': "Укажите номер используемый в Telegram. Для пропуска укажите 0"}
ask_for_telegram_eng = {'msg_start': "Enter your Telegram number. To skip enter 0"}
ask_for_telegram = {rus: ask_for_telegram_ru, eng: ask_for_telegram_eng}

ask_for_viber_ru = {'msg_start': "Укажите номер используемый в Viber. Для пропуска укажите 0"}
ask_for_viber_eng = {'msg_start': "Enter your Viber number. To skip enter 0"}
ask_for_viber = {rus: ask_for_viber_ru, eng: ask_for_viber_eng}

ask_for_local_number_ru = {'msg_start': "Укажите ваш местный номер страны вашего нахождения. Для пропуска укажите 0"}
ask_for_local_number_eng = {'msg_start': "Enter your local number for your current location. To skip enter 0"}
ask_for_local_number = {rus: ask_for_telegram_ru, eng: ask_for_telegram_eng}


saved_your_contacts_ru = {'msg_start': "Сохранили ваши контакты. Теперь с вами смогут связаться, если захотят обмен"}
saved_your_contacts_eng = {'msg_start': "Saved your contacts. Now users can reach you to make an exchange"}
saved_your_contacts = {rus: saved_your_contacts_ru, eng: saved_your_contacts_eng}
