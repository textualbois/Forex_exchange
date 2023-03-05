import sqlite3
from sqlite3 import Error


def connect_and_create(db_file):
    conn = create_connection(db_file)
    create_db_tables(conn)


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
        print(str(e) + "\ngot an error while creating table")


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
                            FIRST_INTERACTION_DATE integer UNIQUE,
                            INTERACTION_COUNT integer,
                            IS_BUSINESS integer,
                            IS_PREMIUM integer,
                            LOC_MAIN_ALIAS TEXT,
                            LOC_MAIN_LAT real,
                            LOC_MAIN_LON real,
                            LOC_ALT1_ALIAS TEXT,
                            LOC_ALT1_LAT real,
                            LOC_ALT1_LON real,
                            LOC_ALT2_ALIAS TEXT,
                            LOC_ALT2_LAT real,
                            LOC_ALT2_LON REAL,
                            AMOUNT_EXCHANGED REAL,
                            REVIEWS_COUNT integer,
                            REVIEWS_MADE integer,
                            PERSONAL_SCORE REAL,
                            WHATSAPP_NUMBER text,
                            TELEGRAM_NUMBER text,
                            VIBER_NUMBER text,
                            LOCAL_NUMBER text,
                            CONTACT_DATA_COMPLETE integer,
                            UNIQUE(USERNAME)
                        );"""

    ACTIVE_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS ACTIVE_BIDS (
                            BID_ID integer Primary KEY,
                            USER_ID integer NOT NULL,
                            IS_PREMIUM integer,
                            CREATED_ON integer NOT NULL,
                            NEED_CUR text NOT NULL,
                            NEED_VAL REAL,
                            NEED_LOC text NOT NULL,
                            HAS_CUR text NOT NULL,
                            HAS_VAL REAL,
                            HAS_LOC text NOT NULL,
                            X_RATE REAL,
                            X_RATE_ALT REAL,
                            LOC_MAIN_ALIAS TEXT,
                            LOC_MAIN_LAT real,
                            LOC_MAIN_LON real,
                            LOC_ALT1_ALIAS TEXT,
                            LOC_ALT1_LAT real,
                            LOC_ALT1_LON real,
                            LOC_ALT2_ALIAS TEXT,
                            LOC_ALT2_LAT real,
                            LOC_ALT2_LON REAL,
                            MUST_COME_TO_ME integer,
                            CARRIED_OVER_BID integer,
                            INTERACTION_PENDING integer
                        );"""

    BIDS_SUMMARY_TABLE = """ CREATE TABLE IF NOT EXISTS BIDS_SUMMARY (
                            BID_ID integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BID_ID2 integer,
                            USER_ID integer NOT NULL,
                            IS_PREMIUM integer,
                            USER_ID2 integer,
                            CREATED_ON integer NOT NULL,
                            STATUS_CHANGE_ON integer,
                            NEED_CUR text NOT NULL,
                            NEED_VAL real,
                            NEED_LOC text,
                            HAS_CUR text NOT NULL,
                            HAS_VAL REAL,
                            HAS_LOC text,
                            X_RATE real,
                            X_RATE_ALT real,
                            X_RATE_FINAL real,
                            X_RATE_FINAL_ALT real,
                            LOC_MAIN_ALIAS TEXT,
                            LOC_MAIN_LAT real,
                            LOC_MAIN_LON real,
                            LOC_ALT1_ALIAS TEXT,
                            LOC_ALT1_LAT real,
                            LOC_ALT1_LON real,
                            LOC_ALT2_ALIAS TEXT,
                            LOC_ALT2_LAT real,
                            LOC_ALT2_LON REAL,
                            MUST_COME_TO_ME integer,
                            BID_STATUS text,
                            CARRIED_OVER_BID integer,
                            INTERACTION_PENDING integer
                        );"""

    FULFILLED_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS FULFILLED_BIDS (
                                BID_ID integer PRIMARY KEY,
                                USER_ID integer,
                                USER_ID2 integer
                        );"""

    CANCELLED_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS CANCELLED_BIDS(
                                BID_ID integer PRIMARY KEY,
                                USER_ID integer
                        );"""

    LOCATION_OF_BIDS_TABLE = """ CREATE TABLE IF NOT EXISTS LOCATION_OF_BIDS (
                                    LOCATION text primary KEY,
                                    ACTIVE_BIDS_COUNT integer,
                                    TOTAL_BIDS_COUNT integer,
                                    FULFILLED_BIDS_COUNT integer,
                                    CANCELLED_BIDS_COUNT integer
                            );"""

    PENDING_REQUESTS_TABLE = """ CREATE TABLE IF NOT EXISTS PENDING_REQUESTS (
                                    BID_ID_ASKERS integer PRIMARY KEY,
                                    BID_ID_BIDDERS integer,
                                    ASKER_ID integer,
                                    BIDDER_ID integer,
                                    ASKER_HAS_REPLIED integer,
                                    AGREEMENT_REACHED integer,
                                    CARRIED_OVER_BID integer,
                                    REQUEST_DATE integer
                            );"""

    create_table(conn, USER_DATA_TABLE)
    create_table(conn, ACTIVE_BIDS_TABLE)
    create_table(conn, BIDS_SUMMARY_TABLE)
    create_table(conn, FULFILLED_BIDS_TABLE)
    create_table(conn, CANCELLED_BIDS_TABLE)
    create_table(conn, LOCATION_OF_BIDS_TABLE)
    create_table(conn, PENDING_REQUESTS_TABLE)
