import sqlite3
from admin_tele_magaz.models import ProductTelegramTable


class ProductTelegram:
    def __init__(self, product_id, category, nom, etre, quantity, prix, img):
        self.product_id = product_id
        self.category = category
        self.nom = nom
        self.etre = etre
        self.quantity = quantity
        self.prix = prix
        self.img = img
        self.products_data_base = []

    def add_product_db(self, author):
        ProductTelegramTable.objects.create(nom=self.nom.title(),
                                            prix=self.prix,
                                            category=self.category,
                                            etre=self.etre, img=self.img,
                                            quantity=self.quantity,
                                            author=author)

    def get_products_db(self):
        self.products_data_base = ProductTelegramTable.objects.all()
