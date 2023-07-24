"""Задание: Есть база данных с двумя таблицами - в первой баланс
пользователя, во второй три мобильных оператора и цена за совершение
звонков. Ежедневно совершается 1 звонок, происходит рандомный выбор
оператора из БД и рандомное количество минут (от 1 до 10).
При выполнении программы происходит 30 рандомных звонков,
данные о них заносятся в csv файл"""


import csv
import datetime
import os.path
import random
import sqlite3

import pytz

moscow_tz = pytz.timezone('Europe/Moscow')
current_time = datetime.datetime.now(moscow_tz)
current_time = current_time.strftime('%H:%M-%d-%m-%Y')

class SqlQueries:

    @staticmethod
    def create_table_users():
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS mobile_users (
                UserID INTEGER PRIMARY KEY,
                User TEXT NOT NULL UNIQUE,
                Balance INTEGER NOT NULL);""")

    @staticmethod
    def create_table_price():
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS mobile_price (
                PriceID INTEGER PRIMARY KEY,
                Mts_Mts INTEGER NOT NULL,
                Mts_Tele2 INTEGER NOT NULL,
                Mts_Yota INTEGER NOT NULL,
                UNIQUE (Mts_Mts, Mts_Tele2, Mts_Yota));""")

    @staticmethod
    def insert_user(user_data):
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO mobile_users
            (User, Balance)
            VALUES (?, ?);""", user_data)

    @staticmethod
    def insert_price(data):
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO mobile_price
            (Mts_Mts, Mts_Tele2, Mts_Yota)
            VALUES (?, ?, ?);""", data)

    @staticmethod
    def get_price():
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Mts_Mts, Mts_Tele2, Mts_Yota
            FROM mobile_price""")
            prices = cur.fetchall()[0]
            return list(prices)

    @staticmethod
    def get_user():
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT User FROM mobile_users
            WHERE UserID = 1""")
            return cur.fetchone()[0]

    @staticmethod
    def get_balance(user):
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance FROM mobile_users
            WHERE User = ?;""", (user,))
            return cur.fetchone()[0]

    @staticmethod
    def update_balance(balance, user):
        with sqlite3.connect('mobile_calls.db') as db:
            cur = db.cursor()
            cur.execute("""UPDATE mobile_users SET Balance = ?
            WHERE User = ?;""", (balance, user,))


class MobileCalls:

    def report_operation(self, data):
        file_exists = os.path.isfile('report_mobile.csv')
        with open('report_mobile.csv', 'a', newline='') as file:
            headers = ['Date', 'Operator', 'Count_min', 'Amount']
            writer = csv.DictWriter(file, delimiter=';', fieldnames=headers)
            if not file_exists:
                writer.writeheader()
                writer.writerow(data)
            else:
                writer.writerow(data)
        print('Данные внесены в отчет\n')


    def program_logic(self):
        SqlQueries.create_table_users()
        SqlQueries.create_table_price()
        SqlQueries.insert_user(('User1', 500))
        SqlQueries.insert_price((1, 2, 3))
        prices = SqlQueries.get_price()
        self.user = SqlQueries.get_user()

        count = 1
        while count < 31:
            self.price = random.choice(prices)
            self.count_min = random.randint(1, 10)
            if self.price == 1:
                self.operator = 'Mts_Mts'
            elif self.price == 2:
                self.operator = 'Mts_Tele2'
            elif self.price == 3:
                self.operator = 'Mts_Yota'

            self.amount = self.price * self.count_min
            self.balance = SqlQueries.get_balance(self.user)
            if self.amount < self.balance:
                self.balance -= self.amount
                SqlQueries.update_balance(self.balance, self.user)
                print(f'{count}. Списано {self.amount} руб, '
                f'оператор {self.operator}, '
                f'стоимость {self.price} руб, количество минут {self.count_min}')
                self.data = ({'Date': current_time, 'Operator': self.operator,
                'Count_min': self.count_min, 'Amount': self.amount})
                self.report_operation(self.data)
            elif self.amount > self.balance:
                print(f'{count}. Недостаточно средств')
                break
            count += 1


start = MobileCalls()
start.program_logic()