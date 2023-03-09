
def parse_callback(call):
	route = call.data.split("_")[0]
	user_input = call.data.split("_")[1]
	secondary_input = call.data.split("__")[1]
	user_id = call.message.chat.id
	message_id = call.message.id
	parsed_callback = {'route': route,
					   'user_input': user_input, 'secondary_input': secondary_input,
					   'user_id': user_id, 'message_id': message_id}
	return parsed_callback


def parse_message(message):
	route = None
	user_input = message
	user_id = message.chat.id
	message_id = message.id
	parsed_message = {'route': route,
					  'user_input': user_input,
					  'user_id': user_id, 'message_id': message_id}
	return parsed_message
