from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import re
import time
from . import password_generator
from . import user
from . import product


def test_page(request):
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request, "test_page.html", context=data)


def hello(request):
    return render(request, "hello.html")


def page_1(request):
    data = {'login': request.POST.get('login')}
    return render(request, "page_1.html", context=data)


def page_2(request):
    data = {'w': request.GET.get('w'), 'r': request.GET.get('r')}
    return render(request, "page_2.html", context=data)


def registration(request):
    error_dict = {'user_login': 'Некорректный логин!',
                  'user_telephone': 'Некорректный телефон!',
                  'user_password': 'Некорректный пароль!',
                  'user_nom': 'Некорректное имя!',
                  'user_prenom': 'Некорректная фамилия!',
                  'double_user': 'Пользователь с таким e-mail или номером '
                                 'телефона уже зарегистрирован!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error}
    return render(request, "registration.html", context=data)


def authorization(request):
    error_dict = {'UserNotFound': 'Пользователь с такими данными не найден!',
                  'LogPassError': 'Некорректный логин или пароль!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error}
    return render(request, "authorization.html", context=data)


def verification(request):
    secur_list = ['delete', 'insert', 'set', 'update', 'drop']
    secur_list_request = [request.GET.get('login'),
                          request.GET.get('telephone'),
                          request.GET.get('password'),
                          request.GET.get('password_repeat'),
                          request.GET.get('nom'),
                          request.GET.get('prenom')]
    for i in secur_list:
        for j in secur_list_request:
            if i in j.lower():
                return redirect('https://www.google.com/')

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
    else:
        user_password = password_generator.generator_de_password(user_password)

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
        current_user = user.User(0, user_nom, user_prenom, user_login,
                                 user_telephone, user_password, 'user')
        current_user.get_users_db()
        if current_user.login not in \
               [element.login for element in current_user.users_data_base] \
               and current_user.telephone not in \
               [element.telephone for element in current_user.users_data_base]:
            current_user.add_user_database()
            time.sleep(3)
            return redirect('/account')
        else:
            return redirect('/registration?error=double_user')
    else:
        temp = {'user_login': user_login, 'user_telephone': user_telephone,
                'user_password': user_password, 'user_nom': user_nom,
                'user_prenom': user_prenom}
        for k, v in temp.items():
            if v == '':
                return redirect(f'/registration?error={k}')


def verification_2(request):
    secur_list = ['delete', 'insert', 'set', 'update', 'drop']
    secur_list_request = [request.GET.get('login'),
                          request.GET.get('password')]
    for i in secur_list:
        for j in secur_list_request:
            if i in j.lower():
                return redirect('https://www.google.com/')

    if re.search(r"\w+\.*\w+@\w+\.\w+", request.GET.get('login')):
        user_login = request.GET.get('login')
    else:
        user_login = ''

    user_password = request.GET.get('password')
    if len(user_password) < 6:
        user_password = ''
    else:
        user_password = password_generator.generator_de_password(user_password)

    if user_login != '' and user_password != '':
        current_user = user.User(0, 'user_nom', 'user_prenom', user_login,
                                 '0123456789', user_password, 'user')
        current_user.get_users_db()
        current_user.get_current_user()
        if current_user.user_id != 0:
            request.session["login"] = current_user.login
            request.session["telephone"] = current_user.telephone
            request.session["password"] = current_user.password
            request.session["nom"] = current_user.nom
            request.session["prenom"] = current_user.prenom
            return redirect('/account')
        else:
            return redirect('/authorization?error=UserNotFound')
    else:
        return redirect('/authorization?error=LogPassError')


def account(request):
    current_user_login = request.session["login"]
    current_user_telephone = request.session["telephone"]
    current_user_password = request.session["password"]
    current_user_nom = request.session["nom"]
    current_user_prenom = request.session["prenom"]
    data = {'current_user_login': current_user_login,
            'current_user_telephone': current_user_telephone,
            'current_user_password': current_user_password,
            'current_user_nom': current_user_nom,
            'current_user_prenom': current_user_prenom}
    return render(request, "account.html", context=data)


def price_list_1(request):
    if request.session.get("_basket_") is None:
        request.session["_basket_"] = []

    some_product = product.Product(0, 'nom', 'etre', '0.0', 'kg', '0.0', 'img')
    some_product.get_products_db()
    data = {'products_all': some_product.products_data_base}
    return render(request, "price_list_1.html", context=data)


def product_info(request):
    product_id = request.GET.get('product_id')
    current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                      'q_2', 0.0, 'img')
    current_product.get_products_db()
    current_product.get_current_product()

    data = {'product_info': current_product}
    return render(request, "product_info.html", context=data)


def add_basket(request):
    product_id = request.GET.get('product_id')
    current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                      'q_2', 0.0, 'img')
    current_product.get_products_db()
    current_product.get_current_product()
    request.session["_basket_"].append(current_product.product_id)
    request.session["_basket_"].sort()
    request.session.modified = True
    next_page_flag = request.GET.get('flag')
    if next_page_flag == '1':
        plus_basket_info = request.GET.get('flag2')
        if plus_basket_info == '1':
            message = 'Товар успешно добавлен в корзину!'
        else:
            message = ''
        data = {'product_info': current_product, 'message': message}
        return render(request, "product_info.html", context=data)
    else:
        plus_basket_info = request.GET.get('flag2')
        if plus_basket_info == '1':
            message = 'Товар успешно добавлен в корзину!'
        else:
            message = ''
        data = {'products_all': current_product.products_data_base,
                'message': message}
        return render(request, "price_list_1.html", context=data)


def basket(request):
    basket_list_id = request.session["_basket_"]
    basket_list = []
    i = 1
    for element in basket_list_id:
        current_product = product.Product(element, 'nom', 'etre', 0.0,
                                          'q_2', 0.0, 'img')
        current_product.get_products_db()
        current_product.get_current_product()
        if element in [j.product_id for j in basket_list]:
            for element_2 in basket_list:
                if element_2.product_id == element:
                    element_2.q_1 += 1
        else:
            current_product.numero = i
            basket_list.append(current_product)
            i += 1
    total_prix = 0
    for element in basket_list:
        element.product_sum = element.prix * element.q_1
        element.product_sum = round(element.product_sum, 2)
        total_prix += element.product_sum
    total_prix = round(total_prix, 2)
    if total_prix != 0:
        message = 'Товары в корзине'
    else:
        message = 'Корзина пуста!'
    data = {'user_basket': basket_list, 'total_prix': total_prix,
            'message': message}
    return render(request, "basket.html", context=data)


def minus_basket(request):
    product_id = request.GET.get('product_id')
    request.session["_basket_"].pop(request.session["_basket_"].index(int(product_id)))
    request.session["_basket_"].sort()
    request.session.modified = True
    return redirect('/basket')


def plus_basket(request):
    product_id = request.GET.get('product_id')
    request.session["_basket_"].append(int(product_id))
    request.session["_basket_"].sort()
    request.session.modified = True
    return redirect('/basket')


def delete_basket(request):
    product_id = request.GET.get('product_id')
    request.session["_basket_"].sort()
    if int(product_id) in request.session["_basket_"]:
        while int(product_id) in request.session["_basket_"]:
            request.session["_basket_"].remove(int(product_id))
    request.session.modified = True
    return redirect('/basket')
