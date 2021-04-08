from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class ProductTelegramTable(models.Model):
    nom = models.CharField(max_length=100)
    quantity = models.CharField(max_length=20)
    numero_quantity = models.FloatField()
    prix = models.FloatField()
    category = models.CharField(max_length=75)


class UserTelegramTable(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    telephone = models.CharField(max_length=13)
    # created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.login
