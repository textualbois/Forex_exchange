from connection import create_connection
from ...config.db_aliases import col_user_id, table_user_data


def update_contact_number(column, user_id, new_value):
    conn = create_connection()
    cur = conn.cursor()
    params = (new_value, user_id)
    query = """
            UPDATE {table_name}
            SET {column_name} = ?
            WHERE {where_column} = ?
            """.format(table_name=table_user_data, column_name=column, where_column=col_user_id)
    cur.execute(query, params)
    conn.commit()
    conn.close()
