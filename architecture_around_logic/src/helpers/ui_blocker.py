from architecture_around_logic.src.connections import bot

"""
clear_inline_keyboard hides used menu buttons
needed to block unwanted inputs from user
"""
def clear_inline_keyboard(user_id, msg_id):
    bot.edit_message_reply_markup(chat_id=user_id,
								  message_id=msg_id,
								  reply_markup=None)
