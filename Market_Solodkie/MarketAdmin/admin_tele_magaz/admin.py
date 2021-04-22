from django.contrib import admin
from .models import ProductTelegramTable, ProductCategoryTable, UserTelegramTable
admin.site.register(ProductTelegramTable)
admin.site.register(ProductCategoryTable)
admin.site.register(UserTelegramTable)
