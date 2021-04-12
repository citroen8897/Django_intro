"""MarketAdmin URL Configuration

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
    path('authorization_solodkie', views.authorization_solodkie),
    path('registration_solodkie', views.registration_solodkie),
    path('account_solodkie', views.account_solodkie),
    path('log_out/', views.log_out),
    path('add_product', views.add_product),
    path('add_category', views.add_category),
    path('verification_category', views.verification_category),
    path('verification_product', views.verification_product)
]
