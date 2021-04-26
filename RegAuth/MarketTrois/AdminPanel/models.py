from django.db import models
from django.utils import timezone


class User(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=13)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.login


class Product(models.Model):
    category = models.CharField(max_length=255)
    nom = models.CharField(max_length=100)
    etre = models.CharField(max_length=25)
    quantity = models.CharField(max_length=35)
    prix = models.FloatField()
    img = models.CharField(max_length=25)
    author = models.CharField(max_length=75)
    published_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom


class Category(models.Model):
    nom = models.CharField(max_length=255)
    author = models.CharField(max_length=75)
    published_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom
