from architecture_around_logic.config.db_aliases import *
from architecture_around_logic.config.dbs import forex_exchange_db as db_file
from architecture_around_logic.src.main_db.connection import create_connection


def store_newbid(USER_ID,
                   NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC,
                   LOC_MAIN_ALIAS, LOC_MAIN_LAT, LOC_MAIN_LON, CREATED_ON):
    conn = create_connection()
    cur = conn.cursor()
    params = (USER_ID,
              NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC,
              LOC_MAIN_ALIAS, LOC_MAIN_LAT, LOC_MAIN_LON, CREATED_ON, bid_is_active)
    query = (f"INSERT OR IGNORE INTO BIDS_SUMMARY "
			 f"(USER_ID, "
			 f"NEED_VAL, HAS_VAL, NEED_CUR, HAS_CUR, NEED_LOC, HAS_LOC, "
			 f"LOC_MAIN_ALIAS, LOC_MAIN_LAT, LOC_MAIN_LON, CREATED_ON, BID_STATUS) "
			 f"VALUES(?,?,?,?,?,?,?,?,?,?,?)")
    cur.execute(query, params)
    conn.commit()
    conn.close()
