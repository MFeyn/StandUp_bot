import sqlite3
import random


def generate_id():
    return random.randint(10000, 99999)


class SQLighter:
    def __init__(self, database):
        """Connect to DB and save connection cursor"""
        self.name = database
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def connection(self):
        return sqlite3.connect(self.name)

    def get_employee(self, nickname):
        self.connection(nickname)
        with self.connection:
            return self.cursor.execute('SELECT * FROM `employees` WHERE `nickname` = ?', (nickname,)).fetchall()

    def is_registered(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `employees` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def is_admin(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `employees` WHERE `user_id` = ? AND `is_admin` = 1',
                                         (user_id,)).fetchall()
            return bool(len(result))

    def add_employee(self, nickname, is_admin=0, total_hours=0):
        with self.connection:
            generated_id = generate_id()
            while True:
                condition = bool(len(self.cursor.execute('SELECT * FROM `employees` WHERE `id` = ?',
                                                         (generated_id,)).fetchall()))
                if condition:
                    generated_id = generate_id()
                else:
                    break

            self.cursor.execute('INSERT INTO `employees` '
                                '(`id`, `is_admin`, `nickname`, `total_hours`) '
                                'VALUES(?, ?, ?, ?)',
                                (generated_id, is_admin, nickname, total_hours,))
            return generated_id

    def register_employee(self, user_id, nickname, password):
        with self.connection:
            condition = self.cursor.execute('SELECT * FROM `employees` WHERE `id` = ? AND `nickname` = ?',
                                            (password, nickname,)).fetchone()
            if condition:
                self.cursor.execute('UPDATE `employees` SET `user_id` = ? WHERE `id` = ?', (user_id, password))
                return True
            else:
                return False

    def change_nickname(self, old_nickname, new_nickname):
        with self.connection:
            return self.cursor.execute('UPDATE `employees` SET `nickname` = ? WHERE `nickname` = ?',
                                       (old_nickname, new_nickname,))

    def change_emp_rights(self, nickname, is_admin):
        with self.connection:
            return self.cursor.execute('UPDATE `employees` SET `is_admin` = ? WHERE `nickname` = ?',
                                       (is_admin, nickname,))

    def del_emp(self, nickname):
        with self.connection:
            return self.cursor.execute('DELETE FROM `employees` WHERE `nickname` = ?', (nickname,))

    def get_total_hours_of_one(self, nickname):
        with self.connection:
            employee_hrs = self.cursor.execute('SELECT `total_hours` FROM `employees` WHERE `nickname` = ?', (nickname,)).fetchone()
            return employee_hrs

    def get_total_hours_of_all(self):
        with self.connection:
            employees = self.cursor.execute('SELECT * FROM `employees`').fetchall()
            keys = []
            values = []
            for row in employees:
                keys.append(row[1])
                values.append(row[4])
            employees_dict = dict(zip(keys, values))
            return employees_dict

    def close(self):
        """Close connection"""
        self.connection.close()
