import os
import telebot
from dotenv import dotenv_values
import sqlite3
from sqlite3 import Error
from rq import job
import message_maker as mm
import project_time_functions
import redis_db as rf


print(".\n..\n...\n....\n.....\n")


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def insert_new_user(db_file, table, prime_key, first_interaction_date):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (prime_key, first_interaction_date)
    query = (f"INSERT OR IGNORE INTO {table} "
             f"(USER_ID, FIRST_INTERACTION_DATE, "
             f"ACTIVE_BIDS_COUNT, TOTAL_BIDS_COUNT, "
             f"CANCELLED_BIDS_COUNT, FULFILLED_BIDS_COUNT) "
             f"VALUES (?, ?, 0, 0, 0, 0)")
    cur.execute(query, params)
    conn.commit()
    conn.close()


def insert_to_cancelled(user_id, bid_id, db_file):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (bid_id, user_id)
    query = (f"INSERT OR IGNORE INTO CANCELLED_BIDS"
             f"(BID_ID, USER_ID)"
             f"VALUES (?,?)")
    cur.execute(query, params)
    conn.commit()
    conn.close()


def insert_to_fulfilled(user_id, bid_id, user_id2, bid_id2, db_file):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (bid_id, user_id, bid_id2, user_id2)
    query = (f"INSERT OR IGNORE INTO FULFILLED_BIDS "
             f"(BID_ID, USER_ID, BID_ID2, USER_ID2) "
             f"VALUES (?,?,?,?)")
    cur.execute(query, params)
    conn.commit()
    conn.close()


# Increment the column value by value
def increment_by_value(db_file, table, prime_key, column, value):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (prime_key, )
    query = (f"UPDATE {table} "
             f"SET {column} = {column} + {value} "
             f"WHERE USER_ID = ?")
    cur.execute(query, params)
    conn.commit()
    conn.close()


# When a new bid is created it stores it into bid summery and active bids
def insert_new_bid(db_file, USER_ID,
                   NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC,
                   LOC_MAIN_ALIAS, LOC_MAIN_LAT, LOC_MAIN_LON, CREATED_ON):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (USER_ID,
              NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC,
              LOC_MAIN_ALIAS, LOC_MAIN_LAT, LOC_MAIN_LON, CREATED_ON)
    for table in ["BIDS_SUMMARY", "ACTIVE_BIDS"]:
        query = (f"INSERT OR IGNORE INTO {table} "
                 f"(USER_ID, "
                 f"NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC, "
                 f"LOC_MAIN_ALIAS, LOC_MAIN_LAT, LOC_MAIN_LON, CREATED_ON) "
                 f"VALUES(?,?,?,?,?,?,?,?,?,?,?)")
        cur.execute(query, params)
    conn.commit()
    conn.close()


def store_pending_exchange_using_job(db_file, bid_id_askers, asker_id, bidder_id, bid_id_bidders=None):
    conn = create_connection(db_file)
    cur = conn.cursor()
    time_now = project_time_functions.get_current_time()
    params = (bid_id_askers, bid_id_bidders, asker_id, bidder_id)
    query = (f"INSERT OR IGNORE INTO PENDING_REQUESTS "
             f"(BID_ID_ASKERS, BID_ID_BIDDERS, ASKER_ID, BIDDER_ID) "
             f"VALUES(?,?,?,?)")
    cur.execute(query, params)
    conn.commit()
    conn.close()


def store_pending_exchange_bid_and_bidder(db_file, bid_id_askers, bidder_id):
    conn = create_connection(db_file)
    cur = conn.cursor()
    time_now = project_time_functions.get_current_time()
    params = (bid_id_askers, bidder_id, time_now)
    query = (f"INSERT OR IGNORE INTO PENDING_REQUESTS "
             f"(BID_ID_ASKERS, BIDDER_ID, REQUEST_DATE) "
             f"VALUES(?,?,?)")
    cur.execute(query, params)
    conn.commit()
    conn.close()


def store_pending_exchange(db_file, bid_id_askers, asker_id, bidder_id, bid_id_bidders=None):
    conn = create_connection(db_file)
    cur = conn.cursor()
    time_now = project_time_functions.get_current_time()
    params = (bid_id_askers, bid_id_bidders, asker_id, bidder_id)
    query = (f"INSERT OR IGNORE INTO PENDING_REQUESTS "
             f"(BID_ID_ASKERS, BID_ID_BIDDERS, ASKER_ID, BIDDER_ID) "
             f"VALUES(?,?,?,?)")
    cur.execute(query, params)
    conn.commit()
    conn.close()


def move_bid_to_cancelled(bid_id, user_id, db_file):
    clear_row(bid_id, "BID_ID", db_file, "ACTIVE_BIDS")
    insert_to_cancelled(user_id, bid_id, db_file)
    update_db_value(db_file, "BIDS_SUMMARY", "BID_ID", bid_id, "BID_STATUS", "CANCELLED")
    time_now = project_time_functions.get_current_time()
    update_db_value(db_file, "BIDS_SUMMARY", "BID_ID", bid_id, "STATUS_CHANGE_ON", time_now)
    increment_by_value(db_file, "USER_DATA", user_id, "ACTIVE_BIDS_COUNT", -1)
    increment_by_value(db_file, "USER_DATA", user_id, "CANCELLED_BIDS_COUNT", 1)


def clear_row(bid_id, condition_column, db_file, table):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (bid_id, )
    query = (f"DELETE FROM {table} "
             f"WHERE {condition_column} = ?")
    cur.execute(query, params)
    conn.commit()
    conn.close()


def update_db_value(db_file, table, condition_column, condition_key, column, new_value):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (new_value, condition_key)
    query = """
            UPDATE {table_name}
            SET {column_name} = ?
            WHERE {where_column} = ?
            """.format(table_name=table, column_name=column, where_column=condition_column)
    cur.execute(query, params)
    conn.commit()
    conn.close()


def get_val_db(db_file, table, condition_column, condition_key, column):
    print("GET_VAL_normal")
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (condition_key,)
    query = """
            SELECT {column_name} FROM {table_name}
            WHERE {where_column} = ?
            """.format(table_name=table, column_name=column, where_column=condition_column)
    result = cur.execute(query, params).fetchone()
    conn.close()
    print(f"for row where {condition_column} = {condition_key}, data for {column} is {result}")
    if result is not None:
        return result[0]
    else:
        return None


def get_val_db_order_by(db_file, table, condition_column, condition_key, column, order_by):
    print(f"GET_VAL order by = {order_by}")
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (condition_key,)
    query = """
            SELECT {column_name} FROM {table_name}
            WHERE {where_column} = ?
            ORDER BY {order} ASC
            """.format(table_name=table, column_name=column, where_column=condition_column, order=order_by)
    result = cur.execute(query, params).fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None


def get_bid_data_by_bid_id(db_file, table, bid_id):
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (bid_id)
    query = """
            SELECT USER_ID, BID_ID, NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC, LOC_MAIN_ALIAS
            FROM {table_name}
            WHERE BID_ID = ?
            """.format(table_name=table)
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    if results is not None:
        return [dict(zip(col_names, row)) for row in results]
    else:
        print("get_bid_data_by_bid_id returned no matches")
        return [0]


# todo rename to get_bids_for_active (maybe)
def get_bids_for_message(db_file, table, user_id, shown_data_job_id, limit, order1="CREATED_ON", order2=""):
    offset_job = job.Job.fetch(shown_data_job_id)
    offset = offset_job.result
    print(f'offset = {offset}')
    print(f'limit = {limit}')
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (user_id, offset, limit)
    query = """
            SELECT BID_ID, NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC, LOC_MAIN_ALIAS
            FROM {table_name}
            WHERE USER_ID = ?
            ORDER BY {order_by1} {order_by2}
            LIMIT ?, ?
            """.format(table_name=table, order_by1=order1, order_by2=order2)
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    if results is not None:
        return [dict(zip(col_names, row)) for row in results]
    else:
        print("get_bids_for_message returned no matches")
        return [0]


def get_bids_for_message_cancelled_or_fulfilled(db_file, table, user_id, shown_data_job_id, limit, bid_status,
                                                order1="CREATED_ON", order2=""):
    offset_job = job.Job.fetch(shown_data_job_id)
    offset = offset_job.result
    print(f'offset = {offset}')
    print(f'limit = {limit}')
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (user_id, bid_status, offset, limit)
    query = """
            SELECT BID_ID, NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC, LOC_MAIN_ALIAS
            FROM {table_name}
            WHERE USER_ID = ? AND BID_STATUS = ?
            ORDER BY {order_by1} {order_by2}
            LIMIT ?, ?
            """.format(table_name=table, order_by1=order1, order_by2=order2)
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    print("get_bids_for_message_cancelled_or_fulfilled:")
    print("result:")
    print([dict(zip(col_names, row)) for row in results])
    return [dict(zip(col_names, row)) for row in results]


def get_bid_for_matches_search(db_file, table, bid_id):
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (bid_id, )
    query = (f"SELECT BID_ID, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC, LOC_MAIN_LAT, LOC_MAIN_LON "
             f"FROM {table} "
             f"WHERE BID_ID = ? ")
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    print("get_bid_for_matches_search")
    print(col_names)
    print(results[0])
    print(results)
    print(dict(zip(col_names, results[0])))
    return dict(zip(col_names, results[0]))


def get_bids_for_message_that_match(db_file, table, trimmed_bids_list_job_id) -> list:
    bid_list = job.Job.fetch(trimmed_bids_list_job_id).result
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    print(bid_list)
    join_with = " OR "
    question_marks = join_with.join(["?" for _ in bid_list])
    params = tuple(bid_list)
    query = (f"SELECT BID_ID, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC, LOC_MAIN_LAT, LOC_MAIN_LON, NEED_VAL, HAS_VAL "
             f"FROM {table} "
             f"WHERE BID_ID = {question_marks} ")
    print(query)
    print(params)
    print("|" + question_marks + "|")
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    print("getting matching bids")
    print(col_names)
    print(results)
    return [dict(zip(col_names, row)) for row in results]


# todo add the calculation of exchange rates when user makes a bid and use it to sort
def get_list_of_matching_bid_ids(db_file, table, user_id, constraints_for_query_job_id) -> list:
    print("get_list_of_matching_bids:")
    bid_data = rf.read_hash_all(f"search_data_for_{user_id}")  # ???
    print(f"bid_data: {bid_data}")
    # bid_data = job.Job.fetch(constraints_for_query_job_id).result # возможно выбрать эту строку
    # NEED_VAL = bid_data["NEED_VAL"]
    # HAS_VAL = bid_data["HAS_VAL"]
    NEED_CUR = bid_data["NEED_CUR"]
    HAS_CUR = bid_data["HAS_CUR"]
    NEED_LOC = bid_data["NEED_LOC"]
    HAS_LOC = bid_data["HAS_LOC"]
    MIN_LAT = bid_data["MIN_LAT"]
    MAX_LAT = bid_data["MAX_LAT"]
    MIN_LON = bid_data["MIN_LON"]
    MAX_LON = bid_data["MAX_LAT"]
    conn = create_connection(db_file)
    #conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (HAS_LOC, NEED_LOC, HAS_CUR, NEED_CUR, MIN_LAT, MAX_LAT, MIN_LON, MAX_LON)
    query = """
            SELECT BID_ID
            FROM {table_name}
            WHERE NEED_LOC = ? AND HAS_LOC = ?
            AND NEED_CUR = ? AND HAS_CUR = ?
            AND LOC_MAIN_LAT BETWEEN ? and ?
            AND LOC_MAIN_LON BETWEEN ? and ?
            AND INTERACTION_PENDING = 0
            """.format(table_name=table)
    results = cur.execute(query, params).fetchall()
    conn.close()
    print("results:")
    print(list(results[0]))
    return list(results[0])


def interaction_is_pending_with_bid_job(db_file, bid_data_job_id, pending_status):
    bid_data = job.Job.fetch(bid_data_job_id).result
    bid_id = bid_data["BID_ID"]
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (pending_status, bid_id)
    for table in ["ACTIVE_BIDS", "BIDS_SUMMARY"]:
        query = """
                UPDATE {table_name}
                SET INTERACTION_PENDING = ?
                WHERE BID_ID = ?
                """.format(table_name=table)
        cur.execute(query, params)
    conn.commit()
    conn.close()


def interaction_is_pending(db_file, bid_id, pending_status):
    conn = create_connection(db_file)
    cur = conn.cursor()
    params = (pending_status, bid_id)
    for table in ["ACTIVE_BIDS", "BIDS_SUMMARY"]:
        query = """
                UPDATE {table_name}
                SET INTERACTION_PENDING = ?
                WHERE BID_ID = ?
                """.format(table_name=table)
        cur.execute(query, params)
    conn.commit()
    conn.close()


def get_contact_info(db_file, table, user_id):
    print(f"getting contact info for {user_id}")
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (user_id, )
    query = """
            SELECT USER_ID, WHATSAPP_NUMBER, TELEGRAM_NUMBER, VIBER_NUMBER, LOCAL_NUMBER, CONTACT_DATA_COMPLETE
            FROM {table_name}
            WHERE USER_ID = ?
            """.format(table_name=table)
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    if results is not None:
        print(dict(zip(col_names, results[0])))
        return dict(zip(col_names, results[0]))
    else:
        return [0]


def get_active_bids_count(db_file, user_id):
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (user_id, )
    query = """
            SELECT USER_ID, ACTIVE_BIDS_COUNT
            FROM USER_DATA
            WHERE USER_ID = ?
            """
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    if results is not None:
        print([dict(zip(col_names, row)) for row in results])
        return [dict(zip(col_names, row)) for row in results]
    else:
        print([0])
        return [0]


def get_full_table(db_file, table):
    conn = create_connection(db_file)
    cur = conn.cursor()
    query = """
            SELECT * FROM USER_DATA
            """
    result = cur.execute(query).fetchall()
    conn.close()
    print(result)
    for row in result:
        print(row)


def bids_with_incoming_requests_full_row(user_id, db_file):
    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    params = (user_id, )
    query = (f"SELECT ASKER_ID, BID_ID_ASKERS, BIDDER_ID, BID_ID_BIDDERS, ASKER_HAS_REPLIED"
             f"AGREEMENT_REACHED, CARRIED_OVER_BID, REQUEST_DATE"
             f"FROM PENDING_REQUESTS "
             f"WHERE ASKER_ID = ?")
    results = cur.execute(query, params).fetchall()
    col_names = [i[0] for i in cur.description]
    conn.close()
    if results is not None:
        print([dict(zip(col_names, row)) for row in results])
        return [dict(zip(col_names, row)) for row in results]
    else:
        return [0]


