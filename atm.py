import datetime
import pytz
import sqlite3
import csv
import os.path


moscow_tz = pytz.timezone('Europe/Moscow')
current_time = datetime.datetime.now(moscow_tz)
current_time = current_time.strftime('%H:%M-%d-%m-%Y')

class SqlQueries:

    @staticmethod
    def create_table():
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users_data (
                UserID INTEGER PRIMARY KEY,
                Number_card INTEGER NOT NULL UNIQUE,
                Pin_code INTEGER NOT NULL,
                Balance INTEGER NOT NULL DEFAULT 0
            );""")
            print('Создание таблицы users_data')

    @staticmethod
    def insert_user(data):
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO Users_data (Number_card, Pin_code)
                        VALUES(?, ?);""", data)
            print('Создание нового пользователя')

    @staticmethod
    def check_number_card(number_card):
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Number_card FROM users_data
                        WHERE Number_card = ?;""", (number_card,))
            number_card = cur.fetchone()
            if number_card == None:
                return False
            else:
                return True

    @staticmethod
    def check_pin_code(number_card, pin_code):
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Pin_code FROM users_data
                        WHERE Number_card = ? and Pin_code = ?;""",
                        (number_card, pin_code))
            pin_code = cur.fetchone()
            if pin_code == None:
                return False
            else:
                return True
            
    @staticmethod
    def check_balance(number_card):
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance FROM users_data
                        WHERE Number_card = ?;""", (number_card,))
            balance = cur.fetchone()
            return balance[0]
        
    @staticmethod
    def update_balance(balance, number_card):
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""UPDATE users_data SET Balance = ?
                        WHERE Number_card = ?;""", (balance, number_card,))


class Atm:

    def check_data(self, card, pin):
        if SqlQueries.check_number_card(card)\
            and SqlQueries.check_pin_code(card, pin):
            return True
        else:
            print('Неверный номер карты или пин-код\n')
            return False

    def input_card(self):
        correct_input = False
        while not correct_input:
            self.number_card = input('Введите номер карты (4 цифры): ')
            if len(self.number_card) == 4:
                try:
                    self.number_card = int(self.number_card)
                    correct_input = True
                    return self.number_card
                except:
                    print('Некорректный ввод\n')                   
            else:
                print('Номер карты должен содержать 4 цифры')
                continue

    def input_pin_code(self):
        correct_input = False
        while not correct_input:
            self.pin_code = input('Введите пин-код (4 цифры): ')
            if len(self.pin_code) == 4:
                try:
                    self.pin_code = int(self.pin_code)
                    correct_input = True
                    return self.pin_code
                except:
                    print('Введен некорректный пин-код\n')                   
            else:
                print('Введен некорректный пин-код\n')
                continue

    def input_money(self):
        correct_input = False
        while not correct_input:
            self.amount = input('Введите сумму: ')
            try:
                self.amount = int(self.amount)
                if self.amount > 0:
                    correct_input = True
                else:
                    print('Сумма не может быть меньше 0\n')
                    continue
            except:
                print('Введите число!\n')               
        return self.amount

    def registration_card(self):
        self.data = ()
        self.number_card = self.input_card()
        if SqlQueries.check_number_card(self.number_card):
            print('Карта с таким номером уже существует!\n')
        else:
            self.data += (self.number_card, )
            self.pin_code = self.input_pin_code()
            self.data += (self.pin_code, )
            SqlQueries.insert_user(self.data)
            print('Карта успешно создана')
            data = ({'Date': current_time, 'Number card': self.number_card,
                    'Type operation': 'new card', 'Amount': '',
                    'Payee': ''})
            self.reporting(data)

    def info_balance(self):
        self.number_card = self.input_card()
        self.pin_code = self.input_pin_code()
        if self.check_data(self.number_card, self.pin_code):
            self.balance = SqlQueries.check_balance(self.number_card)
            print(f'У Вас на счету {self.balance}\n')
            data = ({'Date': current_time, 'Number card': self.number_card,
                    'Type operation': 'info', 'Amount': '',
                    'Payee': ''})
            self.reporting(data)
            return self.balance

    def depositing_money(self):
        self.number_card = self.input_card()
        self.pin_code = self.input_pin_code()
        if self.check_data(self.number_card, self.pin_code):
            self.amount = self.input_money()
            self.balance = SqlQueries.check_balance(self.number_card)
            self.balance += self.amount
            SqlQueries.update_balance(self.balance, self.number_card)
            print('Операция прошла успешно')
            data = ({'Date': current_time, 'Number card': self.number_card,
                    'Type operation': 'depositing', 'Amount': self.amount,
                    'Payee': ''})
            self.reporting(data)

    def withdraw_money(self):
        self.number_card = self.input_card()
        self.pin_code = self.input_pin_code()
        if self.check_data(self.number_card, self.pin_code):
            self.amount = self.input_money()
            self.balance = SqlQueries.check_balance(self.number_card)
            if self.amount <= self.balance:
                self.balance -= self.amount
                SqlQueries.update_balance(self.balance, self.number_card)
                print('Операция прошла успешно')
                data = ({'Date': current_time, 'Number card': self.number_card,
                        'Type operation': 'withdraw', 'Amount': self.amount,
                        'Payee': ''})
                self.reporting(data)
            else:
                print('Недостаточно средств\n')

    def get_recipient(self):
        correct_input = False
        while not correct_input:
            self.card_for_transfer = input('Введите номер карты для перевода: ')
            if len(self.card_for_transfer) == 4:
                try:
                    self.card_for_transfer = int(self.card_for_transfer)
                    correct_input = True
                    return self.card_for_transfer
                except:
                    print('Некорректный ввод\n')                   
            else:
                print('Номер карты должен содержать 4 цифры\n')
                continue

    def transfer_money(self):
        self.number_card = self.input_card()
        self.pin_code = self.input_pin_code()
        if self.check_data(self.number_card, self.pin_code):
            card_for_transfer = self.get_recipient()
            if SqlQueries.check_number_card(card_for_transfer):
                if self.number_card != card_for_transfer:
                    self.balance = SqlQueries.check_balance(self.number_card)
                    print(f'У Вас на счету {self.balance}')
                    amount = input('Сумма перевода: ')
                    amount = int(amount)
                    if amount <= self.balance:
                        self.balance -= amount
                        recipient_balance =\
                        SqlQueries.check_balance(card_for_transfer)
                        recipient_balance += amount
                        SqlQueries.update_balance(self.balance,\
                            self.number_card)
                        SqlQueries.update_balance(recipient_balance,\
                            card_for_transfer)
                        print('Операция прошла успешно')
                        data = ({'Date': current_time, 'Number card': self.number_card,
                                'Type operation': 'Transfer', 'Amount': amount,
                                'Payee': card_for_transfer})
                        self.reporting(data)
                    else:
                        print('У Вас недостаточно средств для перевода\n')
                else:
                    print('Невозможно сделать перевод на свой счет\n')
            else:
                print('Карты с таким номером не существует\n')

    def choosing_an_action(self):
        correct_input = False
        while not correct_input:
            self.choice = input('Выберите действие:\n'
                                'Добавить новую карту - 1\n'
                                'Узнать баланс - 2;\n'
                                'Пополнить баланс - 3\n'
                                'Снять наличные - 4\n'
                                'Перевод денежных средств - 5\n'
                                'Выйти - 6: ')
            if self.choice in ['1', '2', '3', '4', '5', '6']:
                correct_input = True
                return self.choice
            else:
                print('Некорректное действие')
                continue

    def reporting(self, data):
        file_exists = os.path.isfile('report.csv')
        
        with open('report.csv', 'a', newline='') as file:
            headers = ['Date', 'Number card', 'Type operation', 'Amount', 'Payee']
            writer = csv.DictWriter(file, delimiter=';', fieldnames=headers)
            if not file_exists:
                writer.writeheader()
                writer.writerow(data)
            else:
                writer.writerow(data)
        print('Данные внесены в отчет\n')

    def program_logic(self):
        SqlQueries.create_table()
        while True:
            self.choice = self.choosing_an_action()

            if self.choice == '1':
                self.registration_card()
            elif self.choice == '2':
                self.info_balance()
            elif self.choice == '3':
                self.depositing_money()
            elif self.choice == '4':
                self.withdraw_money()
            elif self.choice == '5':
                self.transfer_money()
            elif self.choice == '6':
                break

start = Atm()
start.program_logic()