"""mytestsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('page_1', views.page_1),
    path('page_2/', views.page_2),
    path('registration/', views.registration),
    path('verification/', views.verification),
    path('account/', views.account),
    path('authorization/', views.authorization),
    path('verification_2/', views.verification_2),
    path('template_test/', views.test_page),
    path('price_list_1/', views.price_list_1),
    path('product_info/', views.product_info),
    path('add_basket/', views.add_basket),
    path('basket/', views.basket),
    path('minus_basket/', views.minus_basket),
    path('plus_basket/', views.plus_basket),
    path('delete_basket/', views.delete_basket),
    path('finir_acheter_1/', views.finir_acheter_1),
    path('delivery_type', views.delivery_type),
    path('verification_3/', views.verification_3),
    path('delivery_info', views.delivery_info),
    path('verification_4/', views.verification_4),
    path('pay_type', views.pay_type),
    path('verification_5/', views.verification_5),
    path('felicitation', views.felicitation),
    path('delivery', views.delivery),
    path('log_out/', views.log_out),
    path('verification_6', views.verification_6),
    path('admin_account', views.admin_account),
    path('add_product', views.add_product),
    path('verification_7', views.verification_7),
    path('product_card', views.product_card),
    path('verification_8', views.verification_8),
    path('zakaz_card', views.zakaz_card),
    path('verification_9', views.verification_9)
]
