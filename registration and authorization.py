import sqlite3

class SqlQueries:
    
    """Создание БД и таблицы users_data"""
    
    @staticmethod
    def create_table():
        with sqlite3.connect('registration.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users_data (
                        UserID INTEGER PRIMARY KEY,
                        Login TEXT NOT NULL UNIQUE,
                        Password TEXT NOT NULL,
                        Code INTEGER NOT NULL);""")
            print('Создание таблицы users_data')
            
    """Добавление нового пользователя в таблицу users_data"""
            
    @staticmethod
    def insert_user(user_data):
        with sqlite3.connect('registration.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO users_data (Login, Password, Code)
                        VALUES (?, ?, ?);""", user_data)
            
    """Проверка логина"""
            
    @staticmethod
    def check_login(login):
        with sqlite3.connect('registration.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Login FROM users_data
                        WHERE Login = ?;""", (login,))
            result_login = cur.fetchone()
            if result_login == None:
                return False
            else:
#                 print(f'Введен логин {login}')
                return True
            
    """Проверка пароля"""
    
    @staticmethod        
    def check_password(login, password):
        with sqlite3.connect('registration.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Password FROM users_data
                        WHERE Login = ? AND Password = ?;""", (login, password, ))
            result_password = cur.fetchone()
            if result_password == None:
                return False
            else:
#                 print(f'Введен логин {login}')
#                 print(f'Введен пароль {password}')
                return True
            
    """Проверка кодового слова"""
    
    @staticmethod
    def check_code(login, code):
        with sqlite3.connect('registration.db') as db:
            cur = db.cursor()
            cur.execute("""SELECT Code FROM users_data
                        WHERE Login = ? AND Code = ?;""", (login, code, ))
            result_code = cur.fetchone()
            if result_code == None:
                return False
            else:
#                 print(f'Введено кодовое слово {code}')
                return True
                        
    """Изменение пароля"""           
            
    @staticmethod
    def update_password(password, login):
        with sqlite3.connect('registration.db') as db:
            cur = db.cursor()
            cur.execute("""UPDATE users_data SET Password = ?
                        WHERE Login = ?;""", (password, login, ))
            
          
class Registration:
    
    def input_login(self):
        correct_input = False
        while not correct_input:
            self.login = input('Введите логин: ')
            if len(self.login) > 0 and self.login != ' ':
                correct_input = True
            else:
                continue
        return self.login
        
    def input_password(self):
        correct_input = False
        while not correct_input:
            password = input('Введите пароль: ')
            if len(password) > 0 and password != ' ':
                correct_input = True
            else:
                continue
        return password
        
    def input_code(self):
        correct_input = False
        while not correct_input:
            code = input('Введите код: ')
            if len(code) > 0 and code != ' ':
                correct_input = True
            else:
                continue
        return code
            
    def choosing_an_action(self):
        correct_input = False
        while not correct_input:
            choice = input("""Регистрация - введите 1,
Авторизация - 2,
Восстановление пароля - 3,
Выйти - 0: """)
            try:
                choice = int(choice)
            except:
                print('Неверный ввод')
                
            if choice in [1, 2, 3, 0]:
                correct_input = True
            else:
                continue           
        return choice
        
    def registration(self):
        self.user_data = ()
        self.login = self.input_login()
        if SqlQueries.check_login(self.login):
            print('Пользователь с таким логином уже существует!')
        else:
            self.user_data += (self.login, )
            self.password = self.input_password()
            self.user_data += (self.password, )
            self.code = self.input_code()
            self.user_data += (self.code, )
            SqlQueries.insert_user(self.user_data)
            print('Вы успешно зарегистрировались')
                  
    def authorization(self):
        self.login = self.input_login()
        if SqlQueries.check_login(self.login):
            self.password = self.input_password()
            if SqlQueries.check_password(self.login, self.password):
                print('Вы успешно авторизовались')
            else:
                print('Введен неверный пароль')
        else:
            print('Логин не существует')
                        
    def password_recovery(self):
        self.login = self.input_login()
        if SqlQueries.check_login(self.login):
            self.code = self.input_code()
            if SqlQueries.check_code(self.login, self.code):
                self.new_password = self.input_password()
                SqlQueries.update_password(self.new_password, self.login)
                print('Пароль был успешно изменен!')
            else:
                print('Введен неверный код!')
        else:
            print('Введен неверный логин!')
                   
    def program_logic(self):
        SqlQueries.create_table()
        
        SqlQueries.insert_user(('Ivan', 'qwer1234', 1234))
        
        while True:            
            print()
            self.choice = self.choosing_an_action()
            if self.choice == 1:
                print('\nРегистрация')
                self.registration()
            if self.choice == 2:
                print('\nАвторизация')
                self.authorization()
            if self.choice == 3:
                print('\nВосстановление пароля')
                self.password_recovery()
            if self.choice == 0:
                break
                                    
start = Registration()
start.program_logic()