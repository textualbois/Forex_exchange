from architecture_around_logic.src.connections import redis_main as r


def get_newbid_data(user_id):
	result = r.hgetall(user_id)
	print(f"for user {user_id} get_newbid_data returns:")
	print(result)
	return result
