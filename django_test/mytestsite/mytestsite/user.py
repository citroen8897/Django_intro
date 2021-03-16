import mysql.connector
from mysql.connector import Error


class User:
    def __init__(self, user_id, nom, prenom, login, telephone, password,
                 status, discount, total_summ):
        self.user_id = user_id
        self.nom = nom
        self.prenom = prenom
        self.login = login
        self.telephone = telephone
        self.password = password
        self.status = status
        self.discount = discount
        self.total_summ = total_summ
        self.users_data_base = []

    def add_user_database(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_user = "INSERT INTO ASK_market_users" \
                           "(email,telephone,password,nom,prenom," \
                           "status) VALUES(%s,%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                cursor.execute(new_user, (self.login, self.telephone,
                                          self.password, self.nom,
                                          self.prenom, self.status))
                if cursor.lastrowid:
                    print('успешно добавлена запись. id пользователя: ',
                          cursor.lastrowid)
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_users_db(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ASK_market_users")
                row = cursor.fetchone()
                while row is not None:
                    self.users_data_base.append(User(row[0], row[4], row[5],
                                                     row[1], row[2], row[3],
                                                     row[6], row[7], row[8]))
                    row = cursor.fetchone()
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_current_user(self):
        for person in self.users_data_base:
            if self.login == person.login and self.password == person.password:
                self.user_id = person.user_id
                self.nom = person.nom
                self.prenom = person.prenom
                self.login = person.login
                self.password = person.password
                self.telephone = person.telephone
                self.status = person.status
                self.discount = person.discount
                self.total_summ = person.total_summ

    def make_zakaz(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_zakaz = "INSERT INTO ASK_market_billing" \
                            "(summa, status, id_user, delivery_type, " \
                            "delivery_rue, delivery_maison, " \
                            "delivery_appartement, ville, otdelenie," \
                            "pay_type) " \
                            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                delivery_dict = {'NP': 'Новая Почта', 'Kur': 'Куръер'}
                for k, v in delivery_dict.items():
                    if k == self.delivery_type:
                        self.delivery_type = v
                pay_dict = {'cash': 'наличными', 'VisaMaster': 'на карту'}
                for k, v in pay_dict.items():
                    if k == self.pay_type:
                        self.pay_type = v
                cursor.execute(new_zakaz, (self.total_prix, 'в обработке',
                                           self.user_id, self.delivery_type,
                                           self.delivery_rue,
                                           self.delivery_maison,
                                           self.delivery_appartement,
                                           self.ville,
                                           self.otdelenie, self.pay_type))
                if cursor.lastrowid:
                    print('Заказ успешно оформлен.\nНомер заказа: ',
                          cursor.lastrowid)
                    numero_de_zakaz = cursor.lastrowid
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()
        return numero_de_zakaz

    def make_zakaz_full(self, numero_de_zakaz, product_id, q_1, product_nom):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_zakaz = "INSERT INTO ASK_market_full_orders" \
                            "(numero_de_zakaz, product_id, quantity, " \
                            "product_nom, user_id, user_email) " \
                            "VALUES(%s,%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                cursor.execute(new_zakaz, (numero_de_zakaz, product_id, q_1,
                                           product_nom, self.user_id,
                                           self.login))
                if cursor.lastrowid:
                    print('Успешно добавлена запись...', cursor.lastrowid)
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_discount(self):
        self.total_summ += self.total_prix
        if 3000 < self.total_summ < 7000:
            self.discount = 3
        elif 7000 < self.total_summ < 15000:
            self.discount = 7
        elif 15000 < self.total_summ:
            self.discount = 10

        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                discount = f"UPDATE ASK_market_users SET " \
                           f"discount={self.discount} WHERE id={self.user_id}"
                total_summ = f"UPDATE ASK_market_users SET " \
                             f"total_summ={self.total_summ} " \
                             f"WHERE id={self.user_id}"
                cursor = conn.cursor()
                cursor.execute(discount)
                cursor.execute(total_summ)
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def choisir_password(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_password = f"UPDATE ASK_market_users SET " \
                               f"password='{self.password}' " \
                               f"WHERE id={self.user_id}"
                cursor = conn.cursor()
                cursor.execute(new_password)
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()
