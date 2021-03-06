from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import re
import time
# import password_generator


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
        "<div><a href='/page_2?w=88&r=-33'>Вторая ссылка</a></div>"
        "<br><br>"
        f"<p>Логин введенный на предыдущей странице: <h2>{login}</h2></p>")


def page_2(request):
    w = request.GET.get('w')
    r = request.GET.get('r')
    return HttpResponse("<div>Мы на третьей странице</div>"
                        "<br><br>"
                        f"<h3>Переменная w со страницы page_1: {w}</h3>"
                        f"<h3>Переменная r со страницы page_1: {r}</h3>")


def authorization(request):
    return HttpResponse(
        "<form class='test_form' action='/verification' method='get' "
        "style='width: 17%; margin: 0 auto;'>"
        "   <h1>Регистрация</h1>"
        "   <br><br>"
        "   <div>"
        "       <input type='email' placeholder='E-mail' name='login' "
        "required>"
        "   </div>"
        "   <br>"
        "   <div>"
        "       <input type='text' placeholder='Телефон' name='telephone' "
        "required>"
        "   </div>"
        "   <br>"
        "   <div>"
        "       <input type='password' placeholder='Пароль' name='password' "
        "required>"
        "   </div>"
        "   <br>"
        "   <div>"
        "       <input type='password' placeholder='Повторите пароль' "
        "name='password_repeat' required>"
        "   </div>"
        "   <br>"
        "   <div>"
        "       <input type='text' placeholder='Имя' name='nom' required>"
        "   </div>"
        "   <br>"
        "   <div>"
        "       <input type='text' placeholder='Фамилия' name='prenom' "
        "required>"
        "   </div>"
        "   <br>"
        "   <div>"
        "       <button>Зарегистрироваться</button>"
        "   </div>"
        "</form>")


def verification(request):
    if re.search(r"\w+\.*\w+@\w+\.\w+", request.GET.get('login')):
        user_login = request.GET.get('login')
    else:
        user_login = ''

    user_telephone = request.GET.get('telephone')
    for element in user_telephone:
        if not element.isdigit():
            user_telephone = user_telephone.replace(element, "")
    if len(user_telephone) < 10:
        user_telephone = ''
    else:
        if not user_telephone.startswith("+38"):
            user_telephone = "+38" + user_telephone[-10:]

    user_password = request.GET.get('password')
    user_password_repeat = request.GET.get('password_repeat')
    if user_password != user_password_repeat or len(user_password) < 6:
        user_password = ''
    # else:
    #     user_password = password_generator.generator_de_password(user_password)

    user_nom = request.GET.get('nom').title()
    for element in user_nom:
        if not element.isalpha():
            user_nom = ''

    user_prenom = request.GET.get('prenom').title()
    for element in user_prenom:
        if not element.isalpha():
            user_prenom = ''

    if user_login != '' and user_telephone != '' and user_password != '' and \
            user_nom != '' and user_prenom != '':
        request.session["login"] = user_login
        request.session["telephone"] = user_telephone
        request.session["password"] = user_password
        request.session["nom"] = user_nom
        request.session["prenom"] = user_prenom
        # HttpResponse("<p>Верификация успешно пройдена...</p>")
        time.sleep(3)
        return redirect('/account')
    else:
        return HttpResponse("<p>Данные не прошли верификацию!</p>")


def account(request):
    current_user_login = request.session["login"]
    current_user_telephone = request.session["telephone"]
    current_user_password = request.session["password"]
    current_user_nom = request.session["nom"]
    current_user_prenom = request.session["prenom"]
    return HttpResponse("<h2>Личный кабинет</h2>"
                        f"<p>Логин: {current_user_login}</p>"
                        f"<p>Пароль: {current_user_password}</p>"
                        f"<p>Телефон: {current_user_telephone}</p>"
                        f"<p>Имя: {current_user_nom}</p>"
                        f"<p>Фамилия: {current_user_prenom}</p>")
