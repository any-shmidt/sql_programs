"""Задание: есть 3 пользователя и 3 тарифа. Программа
на вход получает период списания по тарифу, сумма списывается
с баланса, пока достаточно средств (нельзя уйти в минус)"""

import sqlite3


class SqlQueries:

    @staticmethod
    def create_table_users():
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS mobile_users (
                UserID INTEGER PRIMARY KEY,
                User_name TEXT NOT NULL UNIQUE,
                Balance INTEGER NOT NULL,
                Mobile_tariff_ref INTEGER NOT NULL,
                Activity TEXT NOT NULL DEFAULT 'Yes');""")
            print('Создание таблицы mobile_users')

    @staticmethod
    def create_table_tariff():
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS mobile_tariff (
                TariffID INTEGER PRIMARY KEY,
                Tariff TEXT NOT NULL UNIQUE,
                Price INTEGER NOT NULL);""")
            print('Создание таблицы mobile_tariff')

    @staticmethod
    def insert_user(user_data):
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO mobile_users 
            (User_name, Balance, Mobile_tariff_ref)
            VALUES (?, ?, ?);""", user_data)

    @staticmethod
    def insert_tariff(tariff_data):
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO mobile_tariff
            (Tariff, Price)
            VALUES (?, ?);""", tariff_data)

    @staticmethod
    def get_status(user):
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Activity FROM mobile_users
            WHERE User_name = ?;""", (user, ))
            status = cur.fetchone()
            return status[0]

    """Получение стоимости тарифа для каждого пользователя"""
    @staticmethod
    def get_price():
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT User_name, Price
            FROM mobile_tariff
            INNER JOIN mobile_users ON TariffID = Mobile_tariff_ref;""")
            return cur.fetchall()

    @staticmethod
    def get_balance(user):
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance FROM mobile_users
            WHERE User_name = ?;""", (user, ))
            balance = cur.fetchone()
            return balance[0]

    @staticmethod
    def update_activity(status, user):
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""UPDATE mobile_users SET Activity = ?
            WHERE User_name = ?;""", (status, user,))

    @staticmethod
    def update_balance(balance, user):
        with sqlite3.connect('mobile.db') as db:
            cur = db.cursor()
            cur.execute("""UPDATE mobile_users SET Balance = ?
            WHERE User_name = ?;""", (balance, user,))


class MobileTariff:

    def get_period(self):
        correct_input = False
        while not correct_input:
            self.period = input('Введите период расчета: ')
            try:
                self.period = int(self.period)
                if self.period > 0:
                    correct_input = True
                    return self.period
                else:
                    print('Период не может быть отрицательным числом или 0')
            except:
                print('Некорректный ввод')

    def program_logic(self):

        SqlQueries.create_table_users()
        SqlQueries.create_table_tariff()
        SqlQueries.insert_user(('User1', 10000, 2))
        SqlQueries.insert_user(('User2', 10000, 3))
        SqlQueries.insert_user(('User3', 10000, 1))
        SqlQueries.insert_tariff(('Standart', 500))
        SqlQueries.insert_tariff(('VIP', 1000))
        SqlQueries.insert_tariff(('Premium', 1500))

        self.pepiod = self.get_period()

        all_users_prices = SqlQueries.get_price()

        for i in range(len(all_users_prices)):
            self.user = all_users_prices[i][0]
            self.status = SqlQueries.get_status(self.user)
            if self.status == 'Yes':
                print(f'{self.user} status is "Yes"')
                self.price = all_users_prices[i][1]
                print(f'For {self.user} price is {self.price}')
                self.balance = SqlQueries.get_balance(self.user)
                print(f'{self.user} balance = {self.balance}')
                if self.balance > self.period * self.price:
                    self.balance = self.balance - self.price * self.period
                    SqlQueries.update_balance(self.balance, self.user)
                    print('Operation was successfully completed')
                    print(f'{self.user} balance has become a {self.balance}\n')
                else:
                    self.max_period = int(self.balance / self.price)
                    self.balance = self.balance - self.max_period * self.price
                    SqlQueries.update_balance(self.balance, self.user)
                    SqlQueries.update_activity('No', self.user)
                    print(f'For {self.user} max period = {self.max_period}')
                    print(f'{self.user} status has become a "No"')
                    print(f'{self.user} balance has become a {self.balance}\n')
            else:
                print(f'{self.user} status is "No"')
                print('Operation cannot be performed\n')
            

start = MobileTariff()
start.program_logic()