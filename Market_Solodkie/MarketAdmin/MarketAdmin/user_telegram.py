import sqlite3
from admin_tele_magaz.models import UserTelegramTable


class UserTelegram:
    def __init__(self, user_id, login, password, telephone, nom, prenom,
                 reg_date):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.telephone = telephone
        self.nom = nom
        self.prenom = prenom
        self.reg_date = reg_date
        self.users_data_base = []

    def add_user_data_base(self):
        try:
            sqlite_connection = sqlite3.connect('db.sqlite3')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            new_user = """INSERT INTO admin_tele_magaz_usertelegramtable(login, 
            password, nom, prenom, telephone) 
            VALUES(?, ?, ?, ?, ?);"""
            cursor.execute(new_user, (self.login, self.password,
                                      self.nom, self.prenom, self.telephone))
            sqlite_connection.commit()
            print("Запись успешно вставлена в таблицу users",
                  cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def get_users_db(self):
        try:
            sqlite_connection = sqlite3.connect('db.sqlite3')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            cursor.execute("SELECT * FROM admin_tele_magaz_usertelegramtable")
            one_result = cursor.fetchone()
            while one_result is not None:
                self.users_data_base.append(UserTelegram(one_result[0],
                                                         one_result[1],
                                                         one_result[2],
                                                         one_result[5],
                                                         one_result[3],
                                                         one_result[4],
                                                         one_result[6][:19]))
                one_result = cursor.fetchone()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def get_current_user(self):
        for person in self.users_data_base:
            if self.login == person.login and self.password == person.password:
                self.user_id = person.user_id
                self.nom = person.nom
                self.prenom = person.prenom
                self.login = person.login
                self.password = person.password
                self.telephone = person.telephone
                self.reg_date = person.reg_date

    def insert_user(self):
        UserTelegramTable.objects.create(login=self.login,
                                         password=self.password,
                                         nom=self.nom,
                                         prenom=self.prenom,
                                         telephone=self.telephone)
