import strings as s


def send_instructions(lang):
	msg_dict = s.send_instructions[lang]
	msg = msg_dict['msg_start']
	return msg


def your_input_is_bad(lang):
	msg_dict = s.input_is_bad[lang]
	msg = msg_dict['msg_start']
	return msg


def what_is_your_whatsapp(lang):
	msg_dict = s.ask_for_whatsapp[lang]
	msg = msg_dict['msg_start']
	return msg


def what_is_your_telegram(lang):
	msg_dict = s.ask_for_telegram[lang]
	msg = msg_dict['msg_start']
	return msg


def what_is_your_viber(lang):
	msg_dict = s.ask_for_viber[lang]
	msg = msg_dict['msg_start']
	return msg


def what_is_your_local_number(lang):
	msg_dict = s.ask_for_local_number[lang]
	msg = msg_dict['msg_start']
	return msg


def saved_your_contacts(lang):
	msg_dict = s.saved_your_contacts[lang]
	msg = msg_dict['msg_start']
	return msg
