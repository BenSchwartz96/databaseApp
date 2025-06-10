import psycopg2

allowed_tables = {"games", "movies"}

# The below function copied from CGPT. Maybe redo by myself. 
def fetch_game_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM games;")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return colnames, rows


def fetch_table_data(table):
    fetch_table_names()
    if table not in allowed_tables:
        raise ValueError("Invalid table name.")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return colnames, rows

# I want to adjust things so that fetch_data always calls fetch_names first, to make sure all the 
# table names are in allowed_tables

def fetch_table_names():
    global allowed_tables
    conn = get_connection()
    cursor = conn.cursor()
    # Line below fetches all table names.
    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');")
    names = cursor.fetchall()
    tableNames = [name[0] for name in names]
    allowed_tables = set(tableNames)
    cursor.close()
    conn.close()
    return tableNames


# Does not need to be imported to main_window because it'll be called within this file by main_window.
def get_connection():
    return psycopg2.connect(
        dbname="testdb", 
        user="postgres", 
        password="thirtean13", 
        host="localhost", 
        port="5432"
    )