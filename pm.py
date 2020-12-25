from Core import actions, register_user, add_new_password, search_pass_by_name, search_obsolete_passwords
from db import *
import Core
import time
import csv

if __name__ == '__main__':
    connection = connect_to_db()
    # Now user successfully logged into db. We can start working

    cur = connection.cursor()

    #  Is this db used before in pm
    user_name, user_email = register_user(connection)

    work = True
    while work:
        print("What should we do?")
        print(actions)
        print()
        act = input()

        if act == "1":
            #  Add new password
            cur = connection.cursor()
            add_new_password(cur)
            connection.commit()

        if act == "2":
            #  Search for password
            search = input("Input pass name: ")
            print(search_pass_by_name(connection=connection, name=search))
            time.sleep(1)
            print()

        if act == "3":
            #  Import from csv
            f_name = input("Input .csv filename: ")  # TODO

        if act == "4":
            # $ - Export to csv
            do_you_sure = input("Do you sure (Y/N)")
            if do_you_sure == "Y":
                cur = connection.cursor()
                passwords = get_all_pass(cur=cur)
                with open(f'passwords(1).csv', 'w', newline='') as csvfile:
                    fieldnames = list(passwords[0].keys())
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect="excel")
                    writer.writeheader()
                    for password in passwords:
                        writer.writerow(password)
            print(colored("Exported successfully", "green"))

        if act == "5":
            cur = connection.cursor()
            print(search_obsolete_passwords(cur=cur))

        if act == "6":
            #  Get password by id
            cur = connection.cursor()
            pass_id = int(input("Input password Id: "))
            password = get_password_by_id(cur=cur, id=pass_id)
            if bool(password):
                print("Password found.")
                print(Core.create_result_table([password]))
                print("Do you want to delete it? (Y/N)")
                ans = input()
                if ans == "Y":
                    delete_password(pass_id=pass_id, cur=cur)

        if act == "7":
            cur = connection.cursor()
            print(Core.get_all_pass_table(cur))

        if act == "q":
            work = False
