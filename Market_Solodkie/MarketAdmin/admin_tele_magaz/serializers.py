from rest_framework import serializers
from .models import UserTelegramTable


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTelegramTable
        fields = ('id', 'login', 'password', 'nom', 'prenom', 'telephone', 'published_date')
