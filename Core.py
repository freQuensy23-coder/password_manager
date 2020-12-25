from prettytable import PrettyTable
from termcolor import colored
from db import is_table_inited, init_table, save_new_password, get_pass_witch_name, get_all_pass, get_pass_with_date_less
import db
import time
import pymysql
from fuzzywuzzy import fuzz
# TODO Use fuzzy Levenshtein version of this packet
import random

# creating table with info about all actions
actions = PrettyTable()
actions.field_names = ["key", "action"]
actions.add_row(["1", "Add new password"])
actions.add_row(["2", "Search for password"])
actions.add_row(["3", "Import from csv"])
actions.add_row(["4", "Export to csv"])
actions.add_row(["5", "Show obsolete passwords"])
actions.add_row(["6", "Get password by id"])
actions.add_row(["7", "Print all passwords"])


def add_new_password(cur):
    name = input("Login: ")
    password = input("Password (leave empty for autogen): ") # TODO Add autogen
    if password == "":
        password = autogen_pass()
    description = input("Description: ")   # TODO Запись пароля точками при вводe
    url = input("url: ")
    logo = "None" # TODO Logo parser
    created_time = int(time.time())
    ttl = int(input("TTL (in month):"))
    save_new_password(name, password, description, url, logo, created_time, ttl, cur=cur)


def register_user(connection):
    table_init = is_table_inited(connection)
    if table_init is False:
        print("You have never use this DB in password manager. Input your name:")
        user_name = input()
        user_email = input("email: ")
        init_table(connection=connection, name=user_name, email=user_email)
        secret_key = input("Now input secret key. Don't forget them, because you will unable to восстановить его ")
        # TODO Шифрование
    else:
        user_name = table_init["name"]
        user_email = table_init["email"]
        # TODO Add last online date. last activity etc
    print(colored(f"Welcome back {user_name}", "green"))
    return user_name, user_email


def search_pass_by_name(connection, name):
    # At first try to find pass with the same name
    cur = connection.cursor()
    stupid_search = get_pass_witch_name(name=name, cursor=cur)
    if bool(stupid_search):
        # If we find smth with the same name
        table = create_result_table(stupid_search)
        return table

    #  If we can't find pass with the SAME name
    passwords = get_all_pass(cur)
    resulted_pass = []
    for password in passwords:
        # compare its
        ratio_name = fuzz.token_set_ratio(name, password["name"])
        ratio_description = fuzz.token_set_ratio(name, password["description"])
        print(password["name"], ratio_name, ratio_description)
        total_ratio = (ratio_name * 6 + ratio_description * 4) / 10
        if total_ratio > 20: # Created time to normal format
            resulted_pass.append(password)  # TODO Add sort by ratio
    table = create_result_table(resulted_pass)
    return table


def create_result_table(res_list: list) -> PrettyTable:
    """Takes list of dict. Field names = dict keys"""
    res_table = PrettyTable()
    try:

        keys = list(res_list[-1].keys())
        res_table.field_names = keys
        for res_dict in res_list:
            values = []
            for key in keys:
                values.append(res_dict[key])
            res_table.add_row(values)
        return res_table
    except IndexError:
        return colored("Nothing found", "red")


def get_all_pass_table(cur):
    """Returns table with all passwords"""
    passs = db.get_all_pass(cur)
    return create_result_table(passs)


def search_obsolete_passwords(cur):
    now = time.time()
    res = db.get_pass_with_date_less(date=now, cur=cur)
    return create_result_table(res)


def autogen_pass(length = 11, alphabet = "ENG+eng+num+sps"):
    """Generate random password"""
    alphabet_langs = alphabet.split("+")
    symbols = ""
    if "RUS" in alphabet_langs:
        symbols += "йцукенгшщзхъфывапролджэячсмитьбю".upper()
    if "rus" in alphabet_langs:
        symbols += "йцукенгшщзхъфывапролджэячсмитьбю"
    if "ENG" in alphabet_langs:
        symbols += "qwertyuiopasdfghjklzxcvbnm".upper()
    if "eng" in alphabet_langs:
        symbols += "qwertyuiopasdfghjklzxcvbnm"
    if "num" in alphabet_langs:
        symbols += "123456789"
    if "sps" in alphabet_langs:
        symbols += "-_*/+."

    password = ""
    for pas_symb in range(length):
        password += random.choice(symbols)
    return password
