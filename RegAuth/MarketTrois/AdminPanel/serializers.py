from rest_framework import serializers
from .models import User, Product, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', 'nom', 'prenom', 'telephone', 'password',
                  'created_at')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'nom', 'etre', 'quantity', 'prix', 'img',
                  'author', 'published_date', 'modified_date')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'nom', 'author', 'published_date', 'modified_date')
