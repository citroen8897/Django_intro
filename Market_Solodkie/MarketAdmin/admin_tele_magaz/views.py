from .models import UserTelegramTable
from .serializers import UserSerializer
from rest_framework import generics


class UserListCreate(generics.ListCreateAPIView):
    queryset = UserTelegramTable.objects.all()
    serializer_class = UserSerializer


class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTelegramTable.objects.all()
    serializer_class = UserSerializer
