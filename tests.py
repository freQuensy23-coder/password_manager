import unittest
from file_IO import save_connection_data, get_connection_data
import os
import db
import pymysql
import Core


class TestUM(unittest.TestCase):
    def setUp(self):
        self.connection = db.connect_to_db()
        self.test_cur = self.connection.cursor()

    def test_load_and_dump_connection_data(self):
        test_f_name = "tdata.dat"
        test_login_data = {"pass": "1231", "host": "localhost", "login": "user", "db": "db"}
        with open(test_f_name, "w"):
            pass  # Delete everything from file
        save_connection_data(
            test_login_data["host"],
            test_login_data["db"],
            test_login_data["login"],
            test_login_data["pass"],
            f_name=test_f_name)
        read_data = get_connection_data(f_name=test_f_name)
        self.assertEqual(read_data, test_login_data)
        os.remove(test_f_name)

    def test_connect_to_db_using_file_data(self):
        data_from_file = get_connection_data()
        if data_from_file is not None:
            connection = db.connect_to_db()
            cur = connection.cursor()
            self.assertTrue(True)
        else:
            self.skipTest("Connection data is not available")

    def test_pass_generator_1(self):
        pass_length = 6
        for pass_length in range(1, 65):
            password = Core.autogen_pass(length=pass_length, alphabet="RUS+rus")
            self.assertEqual(pass_length, len(password))
            self.assertNotIn(member="z", container=password)
        for pass_length in range(1, 65):
            password = Core.autogen_pass(length=pass_length, alphabet="num")
            self.assertEqual(pass_length, len(password))
            self.assertNotIn("a", password)

    def test_get_password_by_id(self):
        id = 1 # TODO
        print(db.get_password_by_id(id, cur=self.test_cur))


if __name__ == '__main__':
    unittest.main()
