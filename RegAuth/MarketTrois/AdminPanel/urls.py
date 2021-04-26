from django.urls import path
from . import views

urlpatterns = [
    path('api/user/', views.UserListCreate.as_view()),
    path('api/user/<int:pk>', views.SingleUserView.as_view()),
    path('api/product/', views.ProductListCreate.as_view()),
    path('api/product/<int:pk>', views.SingleProductView.as_view()),
    path('api/category/', views.CategoryListCreate.as_view()),
    path('api/category/<int:pk>', views.SingleCategoryView.as_view()),
]
