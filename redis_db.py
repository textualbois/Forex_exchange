import os
import telebot
from dotenv import dotenv_values
import redis
from rq import job
import bot_markups as btmrkp
import main_db
import project_time_functions as ptf
import message_maker
import distances_forex as distances
from rq import Queue, Worker

config = dotenv_values(".env")
print("\n\n\n\n\n")
API_KEY = config["API_KEY"]
REDIS_host = config["REDIS_host"]
REDIS_port = int(config["REDIS_port"])
REDIS_DB = int(config["REDIS_db"])
REDIS_QUEUE = int(config["REDIS_queue_db"])
print(f'Redis host is {REDIS_host}\n'
      f'redis port is {REDIS_port}\n'
      f'redis db code is {REDIS_DB}\n'
      f'redis QUEUE code is {REDIS_QUEUE}\n')


bot = telebot.TeleBot(API_KEY)
r = redis.Redis(host=REDIS_host, port=REDIS_port, db=REDIS_DB, decode_responses=True)


bot = telebot.TeleBot(API_KEY)


def start_user(user_id):
    print(f'writing user_id {user_id} hash')
    r.hsetnx(user_id, "USER_ID", user_id)
    r.hset(user_id, "STATUS", 1)


#  todo rename to: update_hash_for_menu
def update_hash(user_id, sub_key, new_val, status_val):
    print(f'writing sub_key {sub_key} with value {new_val} and status {status_val} to user_id {user_id}')
    r.hset(user_id, sub_key, new_val)
    r.hset(user_id, "STATUS", status_val)


def set_status(user_id, value):
    r.hset(user_id, "STATUS", value)


# makes sure the user is active in redis and resets the "shown data" value for him
def reset_shown_data_count(user_id):
    r.hsetnx(user_id, "USER_ID", user_id)
    r.hset(user_id, "SHOWN_DATA", 0)


# moves a value from the main_db to the redis_db for faster reference
def move_from_main_db(user_id, condition_column, column, db_file, table):
    val = main_db.get_val_db(db_file, table, condition_column, user_id, column)
    r.hset(user_id, column, val)
    return val


def store_new_search(user_id, bid_id):
    print(f"Storing New search for user_id: {user_id} and bid_id {bid_id}")
    redis_key = f"search_data_for_{user_id}"
    r.hdel(redis_key, "*")
    r.hset(redis_key, "BLOCK_SEARCHES", 1)
    r.hset(redis_key, "BID_ID", bid_id)


def complete_search_data(search_range_km, user_id, db_file):
    print(f"filling search data for user {user_id}. Radius set to {search_range_km} km")
    redis_key = f"search_data_for_{user_id}"
    bid_id = r.hget(redis_key, "BID_ID")
    bid_data = main_db.get_bid_for_matches_search(db_file, "ACTIVE_BIDS", bid_id)
    lat = float(bid_data["LOC_MAIN_LAT"])
    lon = float(bid_data["LOC_MAIN_LON"])
    lats = distances.latitude_scope(lat, search_range_km)
    lons = distances.longitude_scope(lon, search_range_km)
    print(bid_data)
    # maybe the values will come in handy later
    #r.hset(redis_key, "HAS_VAL", bid_data["HAS_VAL"])
    #r.hset(redis_key, "NEED_VAL", bid_data["NEED_VAL"])
    r.hset(redis_key, "HAS_CUR", bid_data["HAS_CUR"])
    r.hset(redis_key, "NEED_CUR", bid_data["NEED_CUR"])
    r.hset(redis_key, "HAS_LOC", bid_data["HAS_LOC"])
    r.hset(redis_key, "NEED_LOC", bid_data["NEED_LOC"])
    r.hset(redis_key, "MIN_LAT", lats[0])
    r.hset(redis_key, "MAX_LAT", lats[1])
    r.hset(redis_key, "MIN_LON", lons[0])
    r.hset(redis_key, "MAX_LON", lons[1])
    r.hset(redis_key, "BLOCK_SEARCHES", 0)
    return bid_id


def get_trimmed_list(user_id, shown_data_job_id, offset):
    shown_data = job.Job.fetch(shown_data_job_id).result
    redis_key = f"matches_for_{user_id}"
    matching_bids_count = r.llen(redis_key)
    end = min(int(shown_data) + offset, matching_bids_count - 1)
    trimmed_list = r.lrange(redis_key, shown_data, end)
    print("TRIMMED_LIST_INPUT_DATA:")
    print(shown_data, offset, matching_bids_count, end)
    return trimmed_list


# todo find command that inserts the list without for loop
def store_bids_that_match(user_id, bid_list_job):
    print("store_bids_that_match")
    bid_list = job.Job.fetch(bid_list_job).result
    print(f"bid_list to store:\n"
          f"{bid_list}")
    redis_key = f"matches_for_{user_id}"
    r.delete(redis_key)
    for bid in bid_list:
        r.rpush(redis_key, bid)
    return r.llen(redis_key)


def incr_by(user_id, sub_key, value):
    r.hincrby(user_id, sub_key, value)


def redis_list_length(redis_key):
    return r.llen(redis_key)


def read_hash(user_id, sub_key):
    print(f'reading sub_key={sub_key} value from user_id={user_id}')
    return r.hget(user_id, sub_key)


def read_hash_all(key):  # key is user_id in most cases
    print(f'reading all values under key={key}')
    return r.hgetall(key)


def send_check_result(user_id):
    bid_data = read_hash_all(user_id)
    print(bid_data)
    # add a try clause that re-directs the function to a database version
    # or one that copies the db data to redis
    if message_maker.bid_has_values(bid_data):
        msg = message_maker.bid_string_with_values(bid_data)
    else:
        msg = message_maker.bid_string_without_values(bid_data)
    bot.send_message(int(user_id), msg, reply_markup=btmrkp.markup_check_input(user_id))


def transfer_to_main_db(user_id, db_file):
    bid_data = r.hgetall(user_id)
    NEED_VAL = int(bid_data["NEED_VAL"])
    HAS_VAL = int(bid_data["HAS_VAL"])
    NEED_CUR = bid_data["NEED_CUR"]
    HAS_CUR = bid_data["HAS_CUR"]
    NEED_LOC = bid_data["NEED_LOC"]
    HAS_LOC = bid_data["HAS_LOC"]
    LOC_MAIN_ALIAS = bid_data["LOC_MAIN_ALIAS"]
    LOC_MAIN_LAT = bid_data["LOC_MAIN_LAT"]
    LOC_MAIN_LON = bid_data["LOC_MAIN_LON"]
    CREATED_ON = ptf.get_current_time()
    main_db.insert_new_bid(db_file, user_id, NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC,
                           LOC_MAIN_ALIAS, LOC_MAIN_LAT, LOC_MAIN_LON, CREATED_ON)
    main_db.increment_by_value(db_file, "USER_DATA", user_id, "ACTIVE_BIDS_COUNT", 1)
    main_db.increment_by_value(db_file, "USER_DATA", user_id, "TOTAL_BIDS_COUNT", 1)
    main_db.update_db_value(db_file, "BIDS_SUMMARY", "USER_ID", user_id, "BID_STATUS", "ACTIVE")
    print(bid_data)



