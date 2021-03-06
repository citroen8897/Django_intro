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
