from django.urls import path
from . import views

urlpatterns = [
    path('api/documents/', views.DocumentListCreate.as_view()),
    path('api/document/<str:pk>', views.SomeModelDetailView.as_view()),
    path('api/documentsByDate/', views.DocumentsByDateList.as_view()),
    path('api/DocumentListByDate/', views.DocumentListByDateFilter.as_view()),
    path('api/zips/', views.ZipListCreate.as_view()),
    path('api/zip/<str:pk>', views.SomeModelDetailViewZip.as_view()),
]
