from django.urls import path
from . import views

urlpatterns = [
    path('api/user/', views.UserListCreate.as_view()),
    path('api/user/<int:pk>', views.SingleUserView.as_view()),
]
