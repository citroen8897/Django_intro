from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("<div>Hello world!</div><br><br>"
                        "<div><a href='/page_1'>Первая ссылка</a></div>")


def page_1(request):
    return HttpResponse("<div>Hello world_2!</div><br><br>"
                        "<div><a href='/page_2'>Вторая ссылка</a></div>")


def page_2(request):
    return HttpResponse("<div>Мы на третьей странице</div>")
