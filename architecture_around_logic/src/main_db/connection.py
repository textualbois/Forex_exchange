from sqlite3 import connect, Error


def create_connection(db_file):
    conn = None
    try:
        conn = connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn