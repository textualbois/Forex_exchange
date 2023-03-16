from sqlite3 import connect, Error
from architecture_around_logic.config.dbs import forex_exchange_db as db_file


def create_connection():
    conn = None
    try:
        conn = connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
