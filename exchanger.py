import sqlite3

class SqlQueries:
    
    """Создание БД и таблицы users_balance"""
    
    @staticmethod
    def create_table():
        with sqlite3.connect('exchanger.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users_balance (
                        UserID INTEGER UNIQUE,
                        Balance_RUB INTEGER,
                        Balance_USD INTEGER,
                        Balance_EUR INTEGER);""")
            print('Создание таблицы users_balance')
                       
    """Добавление нового пользователя в таблицу users_balance"""
            
    @staticmethod
    def insert_user(user_data):
        with sqlite3.connect('exchanger.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO users_balance
                        (UserID, Balance_RUB, Balance_USD, Balance_EUR)
                        VALUES (?, ?, ?, ?);""", user_data)

    @staticmethod
    def get_user_id():
        with sqlite3.connect('exchanger.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT UserID FROM users_balance""")
            user_id = cur.fetchone()
            return user_id
                    
    @staticmethod
    def check_balance_rub(user_id):
        with sqlite3.connect('exchanger.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance_RUB FROM users_balance
                        WHERE UserID = ?;""", (user_id,))
            balance_rub = cur.fetchone()
            return balance_rub
            
    @staticmethod
    def check_balance_usd(user_id):
        with sqlite3.connect('exchanger.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance_USD FROM users_balance
                        WHERE UserID = ?;""", (user_id,))
            balance_usd = cur.fetchone()
            return balance_usd
        
    @staticmethod
    def check_balance_euro(user_id):
        with sqlite3.connect('exchanger.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Balance_EUR FROM users_balance
                        WHERE UserID = ?;""", (user_id,))
            balance_euro = cur.fetchone()
            return balance_euro
        
    @staticmethod
    def update_user_balance(user_data):
        with sqlite3.connect('exchanger.db') as db:
            cur = db.cursor()
            cur.execute("""UPDATE users_balance SET Balance_RUB = ?, Balance_USD = ?,
                        Balance_EUR = ? WHERE UserID = ?;""", user_data)


class Exchanger:
    
    def greeting(self):
        print("""Добро пожаловать в наш обменный пункт!
Курс валют следующий:
1 USD = 70 RUB
1 EUR = 80 RUB
1 USD = 0.87 EUR
1 EUR = 1.15 USD""")
    
    """Выбор валюты, которую пользователь хочет купить"""
    def choose_currency_to_buy(self):
        correct_input = False
        while not correct_input:
            self.currency_to_buy = input("""Введите, какую валюту хотите приобрести.
1. RUB
2. USD
3. EUR:""")
            try:
                self.currency_to_buy = int(self.currency_to_buy)
            except:
                print('Неверный ввод')
                
            if self.currency_to_buy in [1, 2, 3]:
                correct_input = True
            else:
                continue
        return self.currency_to_buy
    
    def amount_of_money(self):
        correct_input = False
        while not correct_input:
            self.amount = input('Какая сумма Вас интересует?: ')
            try:
                self.amount = int(self.amount)
                if self.amount >= 0:
                    correct_input = True
                else:
                    print('Сумма не может быть меньше 0')
                    continue
            except:
                print('Введите число!')               
        return self.amount
    
    """Выбор валюты, которую пользователь хочет продать"""
    def choosing_currency_to_sell(self):
        correct_input = False
        while not correct_input:
            self.currency_to_sell = input("""Какую валюту готовы предложить взамен?
1. RUB
2. USD
3. EUR: """)
            try:
                self.currency_to_sell = int(self.currency_to_sell)
            except:
                print('Неверный ввод')
            
            if self.currency_to_sell in [1, 2, 3] and self.currency_to_sell != self.currency_to_buy:
                correct_input = True
            if self.currency_to_sell == self.currency_to_buy:
                print('Данная операция невозможна! Нельзя произвести обмен двух одинаковых валют!')
            else:
                continue
        return self.currency_to_sell
    
    def convert_usd_to_rub(self):
        if self.balance_usd >= self.amount / 70:
            self.balance_rub += self.amount
            self.balance_usd -= self.amount * 0.0143
            user_data = (self.balance_rub, self.balance_usd, self.balance_euro, self.user_id)
            SqlQueries.update_user_balance(user_data)
            print('Операция прошла успешно')
        else:
            print('Операция невозможна, недостаточно средств для обмена')
                        
    def convert_euro_to_rub(self):
        if self.balance_euro >= self.amount / 80:
            self.balance_rub += self.amount
            self.balance_euro -= self.amount * 0.0125
            user_data = (self.balance_rub, self.balance_usd, self.balance_euro, self.user_id)
            SqlQueries.update_user_balance(user_data)
            print('Операция прошла успешно')
        else:
            print('Операция невозможна, недостаточно средств для обмена')
                        
    def convert_usd_to_euro(self):
        if self.balance_usd >= 1.15 * self.amount:
            self.balance_usd -= 1.15 * self.amount
            self.balance_euro += self.amount
            user_data = (self.balance_rub, self.balance_usd, self.balance_euro, self.user_id)
            SqlQueries.update_user_balance(user_data)
            print('Операция прошла успешно')
        else:
            print('Операция невозможна, недостаточно средств для обмена')
                        
    def convert_euro_to_usd(self):
        if self.balance_euro >= 0.87 * self.amount:
            self.balance_euro -= 0.87 * self.amount
            self.balance_usd += self.amount
            user_data = (self.balance_rub, self.balance_usd, self.balance_euro, self.user_id)
            SqlQueries.update_user_balance(user_data)
            print('Операция прошла успешно')
        else:
            print('Операция невозможна, недостаточно средств для обмена')
                        
    def convert_rub_to_usd(self):
        if self.balance_rub >= self.amount * 70:
            self.balance_rub -= self.amount * 70
            self.balance_usd += self.amount
            user_data = (self.balance_rub, self.balance_usd, self.balance_euro, self.user_id)
            SqlQueries.update_user_balance(user_data)
            print('Операция прошла успешно')
        else:
            print('Операция невозможна, недостаточно средств для обмена')
            
    def convert_rub_to_euro(self):
        if self.balance_rub >= self.amount * 80:
            self.balance_rub -= self.amount * 80
            self.balance_euro += self.amount
            user_data = (self.balance_rub, self.balance_usd, self.balance_euro, self.user_id)
            SqlQueries.update_user_balance(user_data)
            print('Операция прошла успешно')
        else:
            print('Операция невозможна, недостаточно средств для обмена')
    
    def program_logic(self):
        SqlQueries.create_table()        
        SqlQueries.insert_user((1, 100000, 1000, 1000))        
        self.greeting()
            
        self.user_id = SqlQueries.get_user_id()[0]
        
        self.currency_to_buy = self.choose_currency_to_buy()
        self.amount = self.amount_of_money()
        self.currency_to_sell = self.choosing_currency_to_sell()
            
        self.balance_rub = SqlQueries.check_balance_rub(self.user_id)[0]
        self.balance_usd = SqlQueries.check_balance_usd(self.user_id)[0]
        self.balance_euro = SqlQueries.check_balance_euro(self.user_id)[0]

        if self.currency_to_buy == 1 and self.currency_to_sell == 2:
            self.convert_usd_to_rub()
        if self.currency_to_buy == 1 and self.currency_to_sell == 3:
            self.convert_euro_to_rub()
        if self.currency_to_buy == 3 and self.currency_to_sell == 2:
            self.convert_usd_to_euro()
        if self.currency_to_buy == 2 and self.currency_to_sell == 3:
            self.convert_euro_to_usd()
        if self.currency_to_buy == 2 and self.currency_to_sell == 1:
            self.convert_rub_to_usd()
        if self.currency_to_buy == 3 and self.currency_to_sell == 1:
            self.convert_rub_to_euro()
                                                
start = Exchanger()
start.program_logic()