import redis_db as rf_glob
from architecture_around_logic.config.user_states import user_state

"""
Partial state machine
helps route classic messages
callbacks (menu buttons) have current state built-in at the markups level
"""


def switch_state(user_id, new_state):
	rf_glob.set_status(user_id, new_state)


def clear_state(user_id, new_state=0):
	rf_glob.set_status(user_id, new_state)


def get_state(user_id):
	rf_glob.read_hash(user_id, user_state)
