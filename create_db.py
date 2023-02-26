import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql_code):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql_code)
        cur.close()
    except Error as e:
        print(e)


def create_db_tables(conn):
    USER_DATA_TABLE = """ CREATE TABLE IF NOT EXISTS USER_DATA (
                            USER_ID integer PRIMARY KEY,
                            USERNAME text,
                            NAME text,
                            SURNAME text,
                            TOTAL_BIDS_COUNT integer,
                            ACTIVE_BIDS_COUNT integer,
                            FULFILLED_BIDS_COUNT integer,
                            CANCELLED_BIDS_COUNT integer,
                            DATE_BORN text,
                            INTERACTION_COUNT integer,
                            IS_BUSINESS integer,
                            LOC_MAIN text,
                            LOC_MAIN_LINK text, 
                            LOC_ALT1 text,
                            LOC_ALT1_LINK text,
                            LOC_ALT2 text,
                            LOC_ALT2_LINK text,
                            AMOUNT_EXCHANGED REAL,
                            REVIEWS_COUNT integer,
                            REVIEWS_MADE integer,
                            PERSONAL_SCORE REAL,
                            UNIQUE(USER_ID)
                        );"""

    ACTIVE_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS ACTIVE_BIDS (
                            BID_ID integer Primary KEY,
                            USER_ID integer,
                            NEED_CUR text,
                            NEED_VAL REAL,
                            NEED_LOC text,
                            HAS_CUR text,
                            HAS_VAL REAL,
                            HAS_LOC text,
                            X_RATE REAL,
                            X_RATE_ALT REAL,
                            LOC_MAIN text,
                            LOC_MAIN_LINK text,
                            LOC_ALT1 text,
                            LOC_ALT1_LINK text,
                            LOC_ALT2 text,
                            LOC_ALT2_LINK text,
                            MUST_COME_TO_ME integer,
                            CARRIED_OVER_BID integer
                        );"""

    BIDS_SUMMERY_TABLE = """ CREATE TABLE IF NOT EXISTS BIDS_SUMMERY (
                            BID_ID integer PRIMARY KEY,
                            USER_ID integer,
                            NEED_CUR text,
                            NEED_VAL REAL,
                            NEED_LOC text,
                            HAS_CUR text,
                            HAS_VAL REAL,
                            HAS_LOC text,
                            X_RATE REAL,
                            X_RATE_ALT REAL,
                            LOC_MAIN text,
                            LOC_MAIN_LINK text,
                            LOC_ALT1 text,
                            LOC_ALT1_LINK text,
                            LOC_ALT2 text,
                            LOC_ALT2_LINK text,
                            MUST_COME_TO_ME integer,
                            CARRIED_OVER_BID integer
                        );"""

    FULLFILLED_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS FULFILLED_BIDS (
                                BID_ID integer PRIMARY KEY
                        );"""

    CANCELLED_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS CANCELLED_BIDS(
                                BID_ID integer PRIMARY KEY,
                                CARRIED_OVER_BID integer
                        );"""

    LOCATION_OF_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS LOCATION_OF_BIDS (
                                    LOCATION text primary KEY,
                                    ACTIVE_BIDS_COUNT integer,
                                    TOTAL_BIDS_COUNT integer,
                                    FULFILLED_BIDS_COUNT integer,
                                    CANCELLED_BIDS_COUNT integer
                            );"""

    FULLFILLED_BIDS_TABLE = """
    """
    CONVERSATIONS_TABLE = """ CREATE TABLE IF NOT EXISTS CONVERSATIONS(
                                BID_ID integer PRIMARY KEY,
                                CARRIED_OVER_BID integer
                        );"""

    create_table(conn, USER_DATA_TABLE)
    #create_table(conn, TEMP_BID_DATA)