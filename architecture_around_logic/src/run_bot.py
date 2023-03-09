from connections import bot, run_bot
from api import parse_callback, parse_message



@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
	parsed_input = parse_callback(call)
	route_callback(parsed_input)


@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
	parsed_input = parse_message(message)
	route_message(parsed_input)


run_bot()