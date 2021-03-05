from django.http import HttpResponse
import re
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


def page_3(request):
    return HttpResponse(
        "<form class='test_form' action='/page_4' method='get' "
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


def page_4(request):
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
        print(user_login, user_telephone, user_password, user_nom, user_prenom)
    # request.session["user"] = login
    return HttpResponse(
        "<div>Данные авторизации</div><br><br>"
        "<br><br>"
        f"<p>Логин введенный на предыдущей странице: <h2>{user_login}</h2></p>"
        f"<p>Пароль введенный на предыдущей странице: "
        f"<h2>{user_password}</h2></p>")
