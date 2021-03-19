import mysql.connector
from mysql.connector import Error


class Product:
    def __init__(self, product_id, nom, etre, q_1, q_2, prix, img):
        self.product_id = product_id
        self.nom = nom
        self.etre = etre
        self.q_1 = q_1
        self.q_2 = q_2
        self.prix = prix
        self.img = img
        self.products_data_base = []

    def get_products_db(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ASK_market_products")
                row = cursor.fetchone()
                while row is not None:
                    self.products_data_base.append(Product(row[0], row[1],
                                                           row[2], row[3],
                                                           row[4], row[5],
                                                           row[6]))
                    row = cursor.fetchone()
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_current_product(self):
        for element in self.products_data_base:
            if element.product_id == self.product_id:
                self.nom = element.nom
                self.etre = element.etre
                self.q_1 = element.q_1
                self.q_2 = element.q_2
                self.prix = element.prix
                self.img = element.img

    def add_product_data_base(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_product = "INSERT INTO ASK_market_products" \
                           "(nom,etre,q_1,q_2,prix,img) " \
                           "VALUES(%s,%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                cursor.execute(new_product, (self.nom, self.etre,
                                             self.q_1, self.q_2,
                                             self.prix, self.img))
                if cursor.lastrowid:
                    print('успешно добавлена запись. id товара: ',
                          cursor.lastrowid)
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def choisir_nom(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_param_de_product = f"UPDATE ASK_market_products SET " \
                                       f"nom='{self.nom}' " \
                                       f"WHERE id={self.product_id}"
                cursor = conn.cursor()
                cursor.execute(new_param_de_product)
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def choisir_prix(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_param_de_product = f"UPDATE ASK_market_products SET " \
                                       f"prix='{self.prix}' " \
                                       f"WHERE id={self.product_id}"
                cursor = conn.cursor()
                cursor.execute(new_param_de_product)
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def choisir_etre(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_param_de_product = f"UPDATE ASK_market_products SET " \
                                       f"etre='{self.etre}' " \
                                       f"WHERE id={self.product_id}"
                cursor = conn.cursor()
                cursor.execute(new_param_de_product)
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()
