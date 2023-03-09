import telebot
from architecture_around_logic.config import bot_api_key

bot = telebot.TeleBot(bot_api_key)

def run_bot():
	bot.polling()