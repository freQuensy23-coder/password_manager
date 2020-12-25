from file_IO import save_connection_data, get_connection_data
import pymysql
from pymysql.cursors import DictCursor
from termcolor import colored


def connect_to_db():
    try_to_connect = True
    first_time_file = True  # We try to connect using file login and pass, but only once
    while try_to_connect:
        conn_data = get_connection_data()
        use_file_data = bool(conn_data) and first_time_file

        if not use_file_data:
            print("Enter mysql DB ip, login and password")
            host = input("Host: ")
            db = input("DB name: ")
            login = input("Login: ")
            password = input("Pass: ")
            print("Connecting")
        else:
            host = conn_data["host"]
            login = conn_data["login"]
            password = conn_data["pass"]
            db = conn_data["db"]

        try:
            connection = pymysql.connect(
                host=host,
                user=login,
                password=password,
                db=db,
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            if use_file_data:
                save_to_file = "F"
            else:
                save_to_file = input("Do you want to save connection data? (It causes some risks)(Y/N)")
            if save_to_file == "Y":
                save_connection_data(host, db, login, password)
            return connection
        except pymysql.err.OperationalError as e:
            # If user input wrong login data
            print(colored("WRONG LOGIN DATA", "red"), e)
            print("Please try again")
            first_time_file = False


def init_table(connection, name: str, email: str):
    cursor = connection.cursor()
    reg_status = "registreted"
    queries = ["""CREATE TABLE IF NOT EXISTS init
            (name TEXT, email TEXT, status TEXT); """,
               """
            CREATE TABLE IF NOT EXISTS passwords
            (id integer AUTO_INCREMENT primary key, name TEXT, password TEXT, description TEXT, url TEXT, logo TEXT, created INTEGER, working INTEGER)
    """, f"""INSERT INTO  init(name, email, status) VALUES ('{name}', '{email}', '{reg_status}')"""]

    for query in queries:
        cursor.execute(query)
    connection.commit()


def is_table_inited(connection):
    """Return False if table is not inited before and user data otherwise"""
    query = """SELECT * FROM init"""
    cur = connection.cursor()
    try:
        cur.execute(query)
        init_data = cur.fetchone()
        return init_data
    except pymysql.err.ProgrammingError:
        return False  # If there is no table with init name


def save_new_password(name: str, password: str, description: str, url: str, logo: str, created: int, working: int, cur):
    query = f"""
    INSERT INTO passwords(name, password, description, url, logo, created, working) 
    VALUES ('{name}', '{password}', '{description}', '{url}', '{logo}', {int(created)}, {int(created) + from_month_to_sec(int(working))})
    """
    cur.execute(query)


def get_pass_witch_name(name: str, cursor) -> list:
    query = f"""
        SELECT * FROM passwords 
        WHERE name = '{name}'
        ORDER BY created
        """
    # TODO Sorted by created downgrade (So at first should be new pass
    cursor.execute(query)
    return cursor.fetchall()


def get_pass_with_date_less(cur, date):
    """Returns all pass with working <= date"""
    query = f"""
        SELECT * FROM passwords
        WHERE working < {date}
    """
    cur.execute(query)
    return cur.fetchall()


def get_all_pass(cur) -> list:
    """Get ALL password from database"""
    query = """SELECT * FROM passwords"""
    cur.execute(query)
    return cur.fetchall()


def from_month_to_sec(month: int) -> int:
    return month * 30 * 24 * 60 * 60


def get_password_by_id(pass_id: int, cur) -> dict:
    query = f"""SELECT * FROM passwords WHERE id = {pass_id}"""
    cur.execute(query)
    return cur.fetchone()


def delete_password(pass_id: int, cur):
    query = f"""DELETE FROM passwords
                WHERE id = {pass_id}"""
    cur.execute(query=query)
