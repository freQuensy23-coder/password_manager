import json


def save_connection_data(host, db, login, password, f_name="connection.json"):
    with open(f_name, "w") as f:
        data_dict = {"host": host, "db": db, "login": login, "pass": password}
        json.dump(data_dict, fp=f)


def get_connection_data(f_name="connection.json"):
    try:
        with open(f_name, "r") as f:
            return json.load(fp=f)
    except FileNotFoundError:
        return None