from connections import bot, run_bot
from api import parse_callback, parse_message, route_callback, route_message




@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
	parsed_input = parse_callback(call)
	route_callback(parsed_input['route'],
				   parsed_input['user_input'], parsed_input['secondary_input'],
				   parsed_input['user_id'], parsed_input['message_id'])


@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
	parsed_input = parse_message(message)
	route_message(parsed_input['route'],
				   parsed_input['user_input'],
				   parsed_input['user_id'], parsed_input['message_id'])


run_bot()
