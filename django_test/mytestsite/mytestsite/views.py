from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse(
        "<form class='test_form' action='/page_1' method='get'>"
        "   <h1>Hello world!</h1>"
        "   <br><br>"
        "   <div>"
        "       <input type='text' placeholder='Логин' name='login' required>"
        "   </div>"
        "   <br><br>"
        "   <div>"
        "       <button>Первая ссылка</button>"
        "   </div>"
        "</form>")


def page_1(request):
    login = request.GET.get('login')
    return HttpResponse(
        "<div>Hello world_2!</div><br><br>"
        "<div><a href='/page_2'>Вторая ссылка</a></div>"
        "<br><br>"
        f"<p>Логин введенный на предыдущей странице: <h2>{login}</h2></p>")


def page_2(request):
    return HttpResponse("<div>Мы на третьей странице</div>")
