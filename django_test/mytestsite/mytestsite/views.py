from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import re
import time
from . import password_generator
from . import user
from . import product
from . import secur


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
        if secur.secur_x(error) == 0:
            return redirect('https://www.google.com/')
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
        if secur.secur_x(error) == 0:
            return redirect('https://www.google.com/')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error}
    return render(request, "authorization.html", context=data)


def verification(request):
    if secur.secur_x(request.GET.get('login')) == 0 or \
            secur.secur_x(request.GET.get('telephone')) == 0 or \
            secur.secur_x(request.GET.get('password')) == 0 or \
            secur.secur_x(request.GET.get('password_repeat')) == 0 or \
            secur.secur_x(request.GET.get('nom')) == 0 or \
            secur.secur_x(request.GET.get('prenom')) == 0:
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
                                 user_telephone, user_password, 'user', 0, 0)
        current_user.get_users_db()
        if current_user.login not in \
               [element.login for element in current_user.users_data_base] \
               and current_user.telephone not in \
               [element.telephone for element in current_user.users_data_base]:
            current_user.add_user_database()
            time.sleep(3)
            return redirect('/authorization')
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
    if secur.secur_x(request.GET.get('login')) == 0 or \
            secur.secur_x(request.GET.get('password')) == 0:
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
                                 '0123456789', user_password, 'user', 0, 0)
        current_user.get_users_db()
        current_user.get_current_user()
        if current_user.user_id != 0:
            request.session["user_id"] = current_user.user_id
            request.session["login"] = current_user.login
            request.session["telephone"] = current_user.telephone
            request.session["password"] = current_user.password
            request.session["nom"] = current_user.nom
            request.session["prenom"] = current_user.prenom
            request.session["auth_triger"] = 1
            request.session["discount"] = current_user.discount
            request.session["total_summ"] = current_user.total_summ
            if request.session.get("helper_1") is None:
                return redirect('/account')
            else:
                return redirect('/delivery_type')
        else:
            return redirect('/authorization?error=UserNotFound')
    else:
        return redirect('/authorization?error=LogPassError')


def account(request):
    error_dict = {'UserNotFound': 'Пользователь с такими паролем не найден!',
                  'PassError': 'Некорректный пароль!',
                  'PassChoisir': 'Пароль успешно изменен!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        if secur.secur_x(error) == 0:
            return redirect('https://www.google.com/')
        for k, v in error_dict.items():
            if k == error:
                error = v
    user_login = request.session["login"]
    user_password = request.session["password"]
    current_user = user.User(0, 'user_nom', 'user_prenom', user_login,
                             '0123456789', user_password, 'user', 0, 0)
    current_user.get_users_db()
    current_user.get_current_user()
    auth_triger = request.session["auth_triger"]
    helper_2 = 0
    if request.GET.get('helper_2'):
        if secur.secur_x(request.GET.get('helper_2')) == 0:
            return redirect('https://www.google.com/')
        helper_2 = int(request.GET.get('helper_2'))
    data = {'current_user': current_user, 'helper_2': helper_2,
            'auth_triger': auth_triger, 'error': error}
    return render(request, "account.html", context=data)


def verification_6(request):
    if secur.secur_x(request.GET.get('password_old')) == 0 or \
            secur.secur_x(request.GET.get('password')) == 0 or \
            secur.secur_x(request.GET.get('password_repeat')) == 0:
        return redirect('https://www.google.com/')
    user_password_old = request.GET.get('password_old')
    user_password_new = request.GET.get('password')
    user_password_new_repeat = request.GET.get('password_repeat')
    if len(user_password_old) < 6:
        user_password_old = ''
    else:
        user_password_old = \
            password_generator.generator_de_password(user_password_old)
    if user_password_old != '':
        user_password = user_password_old
        user_login = request.session["login"]
        current_user = user.User(0, 'user_nom', 'user_prenom', user_login,
                                 '0123456789', user_password, 'user', 0, 0)
        current_user.get_users_db()
        current_user.get_current_user()
        if current_user.user_id == 0:
            return redirect('/account/?helper_2=3&error=UserNotFound')
        else:
            if len(user_password_new) < 6 or\
                    user_password_new != user_password_new_repeat:
                return redirect('/account/?helper_2=3&error=PassError')
            else:
                user_password_new = \
                    password_generator.generator_de_password(user_password_new)
                current_user.password = user_password_new
                current_user.choisir_password()
                request.session["password"] = current_user.password
                return redirect('/account/?helper_2=3&error=PassChoisir')
    else:
        return redirect('/account/?helper_2=3&error=PassError')


def log_out(request):
    request.session.clear()
    request.session["_basket_"] = []
    request.session["discount"] = 0
    request.session["auth_triger"] = 0
    return redirect('/price_list_1')


def price_list_1(request):
    if request.session.get("_basket_") is None:
        request.session["_basket_"] = []

    if request.session.get("auth_triger") is None:
        request.session["auth_triger"] = 0

    if request.session.get("discount") is None:
        request.session["discount"] = 0

    some_product = product.Product(0, 'nom', 'etre', '0.0', 'kg', '0.0', 'img')
    some_product.get_products_db()
    auth_triger = request.session["auth_triger"]
    data = {'products_all': some_product.products_data_base,
            'auth_triger': auth_triger}
    return render(request, "price_list_1.html", context=data)


def product_info(request):
    product_id = request.GET.get('product_id')
    if secur.secur_x(product_id) == 0:
        return redirect('https://www.google.com/')
    current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                      'q_2', 0.0, 'img')
    current_product.get_products_db()
    current_product.get_current_product()
    auth_triger = request.session["auth_triger"]
    data = {'product_info': current_product, 'auth_triger': auth_triger}
    return render(request, "product_info.html", context=data)


def add_basket(request):
    product_id = request.GET.get('product_id')
    if secur.secur_x(product_id) == 0:
        return redirect('https://www.google.com/')
    current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                      'q_2', 0.0, 'img')
    current_product.get_products_db()
    current_product.get_current_product()
    request.session["_basket_"].append(current_product.product_id)
    request.session["_basket_"].sort()
    request.session.modified = True
    next_page_flag = request.GET.get('flag')
    if secur.secur_x(next_page_flag) == 0:
        return redirect('https://www.google.com/')
    if next_page_flag == '1':
        plus_basket_info = request.GET.get('flag2')
        if secur.secur_x(plus_basket_info) == 0:
            return redirect('https://www.google.com/')
        if plus_basket_info == '1':
            message = 'Товар успешно добавлен в корзину!'
        else:
            message = ''
        data = {'product_info': current_product, 'message': message}
        return render(request, "product_info.html", context=data)
    else:
        plus_basket_info = request.GET.get('flag2')
        if secur.secur_x(plus_basket_info) == 0:
            return redirect('https://www.google.com/')
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
            if current_product.numero > 2:
                current_product.prix = current_product.prix * 0.95
            basket_list.append(current_product)
            i += 1
    total_prix = 0
    for element in basket_list:
        element.product_sum = element.prix * element.q_1
        element.prix = round(element.prix, 2)
        element.product_sum = round(element.product_sum, 2)
        total_prix += element.product_sum
    total_prix = total_prix * (1 - (request.session["discount"] / 100))
    total_prix = round(total_prix, 2)
    request.session["basket_total_prix"] = total_prix
    if total_prix != 0:
        message = 'Товары в корзине'
    else:
        message = 'Корзина пуста!'
    if request.session["auth_triger"] == 1:
        user_discount = request.session["discount"]
    else:
        user_discount = 0
    auth_triger = request.session["auth_triger"]
    data = {'user_basket': basket_list, 'total_prix': total_prix,
            'message': message, 'user_discount': user_discount,
            'auth_triger': auth_triger}
    return render(request, "basket.html", context=data)


def minus_basket(request):
    product_id = request.GET.get('product_id')
    if secur.secur_x(product_id) == 0:
        return redirect('https://www.google.com/')
    request.session["_basket_"].pop(request.session["_basket_"].
                                    index(int(product_id)))
    request.session["_basket_"].sort()
    request.session.modified = True
    return redirect('/basket')


def plus_basket(request):
    product_id = request.GET.get('product_id')
    if secur.secur_x(product_id) == 0:
        return redirect('https://www.google.com/')
    request.session["_basket_"].append(int(product_id))
    request.session["_basket_"].sort()
    request.session.modified = True
    return redirect('/basket')


def delete_basket(request):
    product_id = request.GET.get('product_id')
    if secur.secur_x(product_id) == 0:
        return redirect('https://www.google.com/')
    request.session["_basket_"].sort()
    if int(product_id) in request.session["_basket_"]:
        while int(product_id) in request.session["_basket_"]:
            request.session["_basket_"].remove(int(product_id))
    request.session.modified = True
    return redirect('/basket')


def finir_acheter_1(request):
    user_triger = request.session["auth_triger"]
    if user_triger == 0:
        request.session["helper_1"] = 0
        return redirect('/authorization')
    else:
        return redirect('/delivery_type')


def delivery_type(request):
    error_dict = {'NonDeliveryType': 'Тип доставки не выбран!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        if secur.secur_x(error) == 0:
            return redirect('https://www.google.com/')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error}
    request.session["helper_1"] = None
    return render(request, "delivery_type.html", context=data)


def verification_3(request):
    user_type_delivery = request.GET.get('deliveryType')
    if secur.secur_x(user_type_delivery) == 0:
        return redirect('https://www.google.com/')
    if user_type_delivery not in ['NP', 'Kur']:
        return redirect('/delivery_type?error=NonDeliveryType')
    else:
        request.session["delivery_type"] = user_type_delivery
        return redirect('/delivery_info')


def delivery_info(request):
    error_dict = {'NonDeliveryInfo': 'Не указана информация для доставки!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        if secur.secur_x(error) == 0:
            return redirect('https://www.google.com/')
        for k, v in error_dict.items():
            if k == error:
                error = v
    if request.session["delivery_type"] == 'Kur':
        data = {'type_delivery': 'Kur', 'error': error}
        return render(request, "delivery_info.html", context=data)
    else:
        data = {'type_delivery': 'NP', 'error': error}
        return render(request, "delivery_info.html", context=data)


def verification_4(request):
    if request.session["delivery_type"] == 'Kur':
        if secur.secur_x(request.GET.get('rue')) == 0 or \
                secur.secur_x(request.GET.get('maison')) == 0 or \
                secur.secur_x(request.GET.get('appartement')) == 0:
            return redirect('https://www.google.com/')
        if request.GET.get('rue') != '' \
                and request.GET.get('maison') != '' \
                and request.GET.get('appartement') != '':
            request.session["delivery_rue"] = request.GET.get('rue')
            request.session["delivery_maison"] = request.GET.get('maison')
            request.session["delivery_appartement"] = \
                request.GET.get('appartement')
            return redirect('/pay_type')
        else:
            return redirect('/delivery_info?error=NonDeliveryInfo')

    else:
        if secur.secur_x(request.GET.get('ville')) == 0 or \
                secur.secur_x(request.GET.get('otdelenie')) == 0:
            return redirect('https://www.google.com/')
        if request.GET.get('ville') != '' \
                and request.GET.get('otdelenie') != '':
            request.session["ville"] = request.GET.get('ville')
            request.session["otdelenie"] = request.GET.get('otdelenie')
            return redirect('/pay_type')
        else:
            return redirect('/delivery_info?error=NonDeliveryInfo')


def pay_type(request):
    error_dict = {'NonPayType': 'Способ оплаты не выбран!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        if secur.secur_x(error) == 0:
            return redirect('https://www.google.com/')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error}
    return render(request, "pay_type.html", context=data)


def verification_5(request):
    user_type_pay = request.GET.get('payType')
    if secur.secur_x(user_type_pay) == 0:
        return redirect('https://www.google.com/')
    if user_type_pay not in ['cash', 'VisaMaster']:
        return redirect('/pay_type?error=NonPayType')
    else:
        request.session["pay_type"] = user_type_pay
        return redirect('/felicitation')


def felicitation(request):
    current_user = user.User(request.session["user_id"],
                             request.session["nom"],
                             request.session["prenom"],
                             request.session["login"],
                             request.session["telephone"],
                             request.session["password"],
                             'user',
                             request.session["discount"],
                             request.session["total_summ"])
    current_user.total_prix = request.session["basket_total_prix"]
    current_user.total_prix = \
        current_user.total_prix * (1 - (current_user.discount / 100))
    current_user.total_prix = round(current_user.total_prix, 2)
    current_user.delivery_type = request.session["delivery_type"]
    if current_user.delivery_type == 'NP':
        current_user.delivery_rue = ''
        current_user.delivery_maison = ''
        current_user.delivery_appartement = ''
        current_user.ville = request.session["ville"]
        current_user.otdelenie = request.session["otdelenie"]
    else:
        current_user.delivery_rue = request.session["delivery_rue"]
        current_user.delivery_maison = request.session["delivery_maison"]
        current_user.delivery_appartement = \
            request.session["delivery_appartement"]
        current_user.ville = ''
        current_user.otdelenie = ''
    current_user.pay_type = request.session["pay_type"]
    numero_de_zakaz = current_user.make_zakaz()
    basket_list_id = request.session["_basket_"]
    basket_list = []
    j = 1
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
            current_product.numero = j
            basket_list.append(current_product)
            j += 1
    for element in basket_list:
        current_user.make_zakaz_full(numero_de_zakaz,
                                     element.product_id, element.q_1,
                                     element.nom)
    current_user.get_discount()
    request.session.clear()
    request.session["_basket_"] = []
    request.session["discount"] = 0
    request.session["auth_triger"] = 0
    data = {'numero_de_zakaz': numero_de_zakaz, 'basket': basket_list,
            'total_prix': current_user.total_prix}
    return render(request, "felicitation.html", context=data)


def delivery(request):
    auth_triger = request.session["auth_triger"]
    data = {'auth_triger': auth_triger}
    return render(request, "delivery.html", context=data)
