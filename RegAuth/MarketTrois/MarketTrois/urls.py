"""MarketTrois URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', include('AdminPanel.urls')),
    path('admin/', admin.site.urls),
    path('authorization/', views.authorization),
    path('registration/', views.registration),
    path('account/', views.account),
    path('add_product/', views.add_product),
    path('verification_product', views.verification_product),
    path('add_category/', views.nouveau_category),
    path('category_card/', views.category_card),
    path('chansir_category_nom/', views.chansir_category_nom),
    path('delete_category/', views.delete_category),
    path('log_out/', views.log_out),
    path('product_card', views.product_card),
    path('verification_product_card', views.verification_product_card),
    path('delete_product', views.delete_product),
    path('verification_chercher', views.verification_chercher)
]
