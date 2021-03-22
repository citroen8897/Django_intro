from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import re
import time
import datetime
import copy
from . import password_generator
from . import user
from . import product
from . import secur
from operator import attrgetter


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
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

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
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

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
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

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
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

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
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    error_dict = {'UserNotFound': 'Пользователь с такими паролем не найден!',
                  'PassError': 'Некорректный пароль!',
                  'PassChoisir': 'Пароль успешно изменен!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
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
        helper_2 = int(request.GET.get('helper_2'))
        if helper_2 == 2:
            current_user.zakazes_data_base = \
                current_user.get_history_des_zakazes()
            for zakaz in current_user.zakazes_data_base:
                zakaz['zakaz_basket'] = \
                    current_user.get_full_info_de_zakaz(zakaz['numero_de_zakaz'])
                current_user.zakazes_data_base.sort(
                    key=lambda zakaz_: zakaz_['date_time'])
                current_user.zakazes_data_base = current_user.zakazes_data_base[
                                                 ::-1]
    if current_user.status == 'user':
        data = {'current_user': current_user, 'helper_2': helper_2,
                'auth_triger': auth_triger, 'error': error,
                'basket': request.session["_basket_"]}
        return render(request, "account.html", context=data)
    elif current_user.status == 'admin':
        some_product = product.Product(0, 'nom', 'etre', '0.0', 'kg', '0.0',
                                       'img')
        some_product.get_products_db()
        products_data_base = some_product.products_data_base
        current_user.zakazes_data_base = \
            current_user.get_history_des_zakazes()
        for zakaz in current_user.zakazes_data_base:
            zakaz['zakaz_basket'] = \
                current_user.get_full_info_de_zakaz(zakaz['numero_de_zakaz'])

        for e in current_user.zakazes_data_base:
            for k, v in e.items():
                if k == 'date_time':
                    e[k] = str(v)

        current_user.zakazes_data_base.sort(
            key=lambda zakaz_: zakaz_['date_time'])
        current_user.zakazes_data_base = current_user.zakazes_data_base[::-1]

        if request.GET.get('zakaz_sort'):
            if request.session['helper_4'] is not None:
                if request.session['helper_4'] == 1:
                    current_user.zakazes_data_base = copy.deepcopy(request.session['zakaz_list_select'])

            if request.GET.get('zakaz_sort') == '0':
                current_user.zakazes_data_base.sort(key=lambda zakaz_: zakaz_['numero_de_zakaz'])
            elif request.GET.get('zakaz_sort') == '1':
                current_user.zakazes_data_base.sort(key=lambda zakaz_: zakaz_['date_time'])
            elif request.GET.get('zakaz_sort') == '2':
                current_user.zakazes_data_base.sort(key=lambda zakaz_: zakaz_['summa'])
                current_user.zakazes_data_base = current_user.zakazes_data_base[::-1]
            elif request.GET.get('zakaz_sort') == '3':
                current_user.zakazes_data_base.sort(key=lambda zakaz_: zakaz_['status_de_zakaz'])
            elif request.GET.get('zakaz_sort') == '4':
                current_user.zakazes_data_base.sort(key=lambda zakaz_: zakaz_['id_user'])
            elif request.GET.get('zakaz_sort') == '5':
                current_user.zakazes_data_base.sort(key=lambda zakaz_: zakaz_['delivery_type'])
            elif request.GET.get('zakaz_sort') == '6':
                current_user.zakazes_data_base.sort(key=lambda zakaz_: zakaz_['pay_type'])

        request.session['zakazes'] = \
            copy.deepcopy(current_user.zakazes_data_base)
        for e in current_user.zakazes_data_base:
            for k, v in e.items():
                if k == 'date_time':
                    e[k] = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

        helper_3 = 0
        if request.GET.get('helper_3'):
            helper_3 = int(request.GET.get('helper_3'))
            if request.GET.get('helper_4'):
                if request.GET.get('helper_4') == '1':
                    date_start = request.GET.get('date_start')
                    date_fin = request.GET.get('date_finish')
                    date_start = datetime.datetime.strptime(date_start,
                                                            '%Y-%m-%d')
                    date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d')
                    date_fin = date_fin + datetime.timedelta(hours=23,
                                                             minutes=59,
                                                             seconds=59)
                    zakazes_date_time_select = []
                    for e in current_user.zakazes_data_base:
                        for k, v in e.items():
                            if k == 'date_time':
                                if date_fin >= v >= date_start:
                                    zakazes_date_time_select.append(e)
                    current_user.zakazes_data_base = copy.deepcopy(zakazes_date_time_select)
                    for e in zakazes_date_time_select:
                        for k, v in e.items():
                            if k == 'date_time':
                                e[k] = str(v)
                    request.session['zakaz_list_select'] = zakazes_date_time_select
            else:
                if request.GET.get('helper_3') and not request.GET.get('zakaz_sort'):
                    request.session['helper_4'] = 0

            if request.GET.get('product_sort'):
                if request.GET.get('product_sort') == '0':
                    products_data_base.sort(key=lambda product_: product_.product_id)
                elif request.GET.get('product_sort') == '1':
                    products_data_base.sort(key=lambda product_: product_.nom)
                elif request.GET.get('product_sort') == '2':
                    products_data_base.sort(key=lambda product_: product_.etre)
                elif request.GET.get('product_sort') == '3':
                    products_data_base.sort(key=lambda product_: product_.prix)
            elif request.GET.get('user_sort'):
                if request.GET.get('user_sort') == '0':
                    current_user.users_data_base.sort(key=lambda user_: user_.user_id)
                elif request.GET.get('user_sort') == '1':
                    current_user.users_data_base.sort(key=lambda user_: user_.prenom)
                elif request.GET.get('user_sort') == '2':
                    current_user.users_data_base.sort(key=attrgetter('nom', 'prenom'))
                elif request.GET.get('user_sort') == '3':
                    current_user.users_data_base.sort(key=lambda user_: user_.login)
                elif request.GET.get('user_sort') == '4':
                    current_user.users_data_base.sort(key=lambda user_: user_.status)
                elif request.GET.get('user_sort') == '5':
                    current_user.users_data_base.sort(key=attrgetter('discount', 'total_summ'))
                    current_user.users_data_base = current_user.users_data_base[::-1]
                elif request.GET.get('user_sort') == '6':
                    current_user.users_data_base.sort(key=lambda user_: user_.total_summ)
                    current_user.users_data_base = current_user.users_data_base[::-1]
        data = {'current_user': current_user, 'helper_3': helper_3,
                'auth_triger': auth_triger, 'error': error,
                'products_data_base': products_data_base}
        return render(request, "admin_account.html", context=data)


def admin_account(request):
    return redirect('/admin_account')


def add_product(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    error_dict = {'product_nom': 'Некорректное название!',
                  'product_q_1': 'Некорректная единица товара!',
                  'product_q_2': 'Некорректная единица измерения товара!',
                  'product_prix': 'Некорректная цена!',
                  'product_img': 'Некорректная ссылка!',
                  'product_status': 'Некорректный статус!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error}
    return render(request, "add_product.html", context=data)


def verification_7(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    product_nom = request.GET.get('nom')
    if len(product_nom) == 0:
        product_nom = ''

    product_q_1 = request.GET.get('q_1')
    if re.findall(r'[^0-9.]', str(product_q_1)) or len(product_q_1) == 0:
        product_q_1 = ''
    else:
        product_q_1 = float(product_q_1)

    product_q_2 = request.GET.get('q_2')
    if len(product_q_2) == 0:
        product_q_2 = ''

    product_prix = request.GET.get('prix')
    if re.findall(r'[^0-9.]', str(product_prix)) or len(product_prix) == 0:
        product_prix = ''
    else:
        product_prix = float(product_prix)

    product_img = request.GET.get('img')
    if len(product_img) == 0:
        product_img = ''

    product_status = request.GET.get('status')
    if product_status not in ['0', '1', '2', '3', '4']:
        product_status = ''
    else:
        status_dict = {'0': 'в наличии', '1': 'нет в наличии',
                       '2': 'ожидается',
                       '3': 'под заказ', '4': 'снят с производства'}
        for k, v in status_dict.items():
            if k == product_status:
                product_status = v
    if product_nom != '' and product_q_1 != '' and product_q_2 != '' and \
            product_prix != '' and product_img != '' and product_status != '':
        nouveau_product = product.Product(0, product_nom, product_status,
                                          product_q_1, product_q_2,
                                          product_prix, product_img)
        nouveau_product.add_product_data_base()
        data = {'error': 'Изменения сохранены'}
        return render(request, "admin_account.html", context=data)
    else:
        temp = {'product_nom': product_nom, 'product_q_1': product_q_1,
                'product_q_2': product_q_2, 'product_prix': product_prix,
                'product_img': product_img, 'product_status': product_status}
        for k, v in temp.items():
            if v == '':
                return redirect(f'/add_product?error={k}')


def product_card(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.GET.get('product_id')
    current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                      'q_2', 0.0, 'img')
    current_product.get_products_db()
    current_product.get_current_product()
    request.session["product_id"] = current_product.product_id
    data = {'product_info': current_product}
    return render(request, "product_card.html", context=data)


def verification_8(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.session["product_id"]

    product_nom = request.GET.get('nom')
    if len(product_nom) == 0:
        product_nom = '0'

    product_prix = request.GET.get('prix')
    if re.findall(r'[^0-9.]', str(product_prix)) or len(product_prix) == 0:
        product_prix = '0'
    else:
        product_prix = float(product_prix)

    product_status = request.GET.get('status')
    if product_status not in ['0', '1', '2', '3', '4']:
        product_status = '0'
    else:
        status_dict = {'0': 'в наличии', '1': 'нет в наличии',
                       '2': 'ожидается',
                       '3': 'под заказ', '4': 'снят с производства'}
        for k, v in status_dict.items():
            if k == product_status:
                product_status = v

    if product_nom != '0':
        current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                          'q_2', 0.0, 'img')
        current_product.get_products_db()
        current_product.get_current_product()
        current_product.nom = product_nom
        current_product.choisir_nom()

    if product_prix != '0':
        current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                          'q_2', 0.0, 'img')
        current_product.get_products_db()
        current_product.get_current_product()
        current_product.prix = product_prix
        current_product.choisir_prix()

    if product_status != '0':
        current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                          'q_2', 0.0, 'img')
        current_product.get_products_db()
        current_product.get_current_product()
        current_product.etre = product_status
        current_product.choisir_etre()
    data = {'error': 'Изменения сохранены'}
    return render(request, "admin_account.html", context=data)


def zakaz_card(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    zakazes_data_base = copy.deepcopy(request.session['zakazes'])
    for e in zakazes_data_base:
        for k, v in e.items():
            if k == 'date_time':
                e[k] = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

    current_zakaz_numero = request.GET.get('numero_de_zakaz')
    for zakaz in zakazes_data_base:
        if str(zakaz['numero_de_zakaz']) == current_zakaz_numero:
            current_zakaz = zakaz
    request.session['numero_de_zakaz'] = current_zakaz_numero

    i = 1
    for t in current_zakaz['zakaz_basket']:
        t['numero'] = i
        i += 1
        # current_product = product.Product(t['tovar_id'], 'nom', 'etre', 0.0,
        #                                   'q_2', 0.0, 'img')
        # current_product.get_products_db()
        # current_product.get_current_product()
        # t['tovar_prix'] = current_product.prix
        current_user = user.User(t['client_id'], 'user_nom', 'user_prenom',
                                 'user_login',
                                 '0123456789', 'user_password', 'user', 0, 0)
        current_user.get_users_db()
        current_user.get_current_user_id()
        t['client_info'] = current_user
    # zakaz_total = 0
    # for t in current_zakaz['zakaz_basket']:
    #     if t['numero'] < 3:
    #         t['tovar_summ'] = round(t['tovar_prix'] * t['quantity'], 2)
    #         zakaz_total += t['tovar_summ']
    #     else:
    #         t['tovar_summ'] = round(t['tovar_prix'] * t['quantity'] * 0.95, 2)
    #         zakaz_total += t['tovar_summ']
    # current_zakaz['zakaz_total'] = round(zakaz_total, 2)
    data = {'current_zakaz': current_zakaz}
    return render(request, "zakaz_card.html", context=data)


def verification_9(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    current_zakaz_numero = request.session['numero_de_zakaz']
    nouveau_status_zakaz = request.GET.get('status')
    if nouveau_status_zakaz not in ['0', '1', '2', '3', '4', '5', '6']:
        nouveau_status_zakaz = '0'
    else:
        status_dict = {'0': 'в обработке', '1': 'обработан',
                       '2': 'отправлен',
                       '3': 'доставлен', '4': 'выполнен',
                       '5': 'отменен', '6': 'отклонен'}
        for k, v in status_dict.items():
            if k == nouveau_status_zakaz:
                nouveau_status_zakaz = v
    if nouveau_status_zakaz != '0':
        user_login = request.session["login"]
        user_password = request.session["password"]
        current_user = user.User(0, 'user_nom', 'user_prenom', user_login,
                                 '0123456789', user_password, 'user', 0, 0)
        current_user.get_users_db()
        current_user.get_current_user()
        current_user.choisir_status_de_zakaz(nouveau_status_zakaz,
                                             current_zakaz_numero)
    data = {'error': 'изменения сохранены'}
    return render(request, "admin_account.html", context=data)


def user_card(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    user_id = request.GET.get('user_id')
    some_user = user.User(int(user_id), 'user_nom', 'user_prenom',
                          'user_login', '0123456789', 'user_password', 'user',
                          0, 0)
    some_user.get_users_db()
    some_user.get_current_user_id()
    zakazes_data_base = copy.deepcopy(request.session['zakazes'])
    for e in zakazes_data_base:
        for k, v in e.items():
            if k == 'date_time':
                e[k] = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
    zakazes_de_current_user = []
    for zakaz in zakazes_data_base:
        if zakaz['id_user'] == int(user_id):
            zakazes_de_current_user.append(zakaz)
    data = {'zakazes_de_current_user': zakazes_de_current_user,
            'some_user': some_user}
    return render(request, "user_card.html", context=data)


def verification_10(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    date_start = request.GET.get('date_start')
    date_fin = request.GET.get('date_finish')
    request.session['helper_4'] = 1
    return redirect(f'/account/?helper_3=3&helper_4=1&date_start={date_start}&date_finish={date_fin}')


def verification_6(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

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
            'auth_triger': auth_triger, 'basket': request.session["_basket_"]}
    return render(request, "price_list_1.html", context=data)


def product_info(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.GET.get('product_id')
    current_product = product.Product(int(product_id), 'nom', 'etre', 0.0,
                                      'q_2', 0.0, 'img')
    current_product.get_products_db()
    current_product.get_current_product()
    auth_triger = request.session["auth_triger"]
    data = {'product_info': current_product, 'auth_triger': auth_triger,
            'basket': request.session["_basket_"]}
    return render(request, "product_info.html", context=data)


def add_basket(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
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
        data = {'product_info': current_product, 'message': message,
                'auth_triger': request.session["auth_triger"],
                'basket': request.session["_basket_"]}
        return render(request, "product_info.html", context=data)
    else:
        plus_basket_info = request.GET.get('flag2')
        if plus_basket_info == '1':
            message = 'Товар успешно добавлен в корзину!'
        else:
            message = ''
        data = {'products_all': current_product.products_data_base,
                'message': message,
                'auth_triger': request.session["auth_triger"],
                'basket': request.session["_basket_"]}
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
            'auth_triger': auth_triger, 'basket': request.session["_basket_"]}
    return render(request, "basket.html", context=data)


def minus_basket(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.GET.get('product_id')
    request.session["_basket_"].pop(request.session["_basket_"].
                                    index(int(product_id)))
    request.session["_basket_"].sort()
    request.session.modified = True
    return redirect('/basket')


def plus_basket(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.GET.get('product_id')
    request.session["_basket_"].append(int(product_id))
    request.session["_basket_"].sort()
    request.session.modified = True
    return redirect('/basket')


def delete_basket(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.GET.get('product_id')
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
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    error_dict = {'NonDeliveryType': 'Тип доставки не выбран!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error, 'basket': request.session["_basket_"]}
    request.session["helper_1"] = None
    return render(request, "delivery_type.html", context=data)


def verification_3(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    user_type_delivery = request.GET.get('deliveryType')
    if user_type_delivery not in ['NP', 'Kur']:
        return redirect('/delivery_type?error=NonDeliveryType')
    else:
        request.session["delivery_type"] = user_type_delivery
        return redirect('/delivery_info')


def delivery_info(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    error_dict = {'NonDeliveryInfo': 'Не указана информация для доставки!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    if request.session["delivery_type"] == 'Kur':
        data = {'type_delivery': 'Kur', 'error': error,
                'basket': request.session["_basket_"]}
        return render(request, "delivery_info.html", context=data)
    else:
        data = {'type_delivery': 'NP', 'error': error,
                'basket': request.session["_basket_"]}
        return render(request, "delivery_info.html", context=data)


def verification_4(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    if request.session["delivery_type"] == 'Kur':
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
        if request.GET.get('ville') != '' \
                and request.GET.get('otdelenie') != '':
            request.session["ville"] = request.GET.get('ville')
            request.session["otdelenie"] = request.GET.get('otdelenie')
            return redirect('/pay_type')
        else:
            return redirect('/delivery_info?error=NonDeliveryInfo')


def pay_type(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    error_dict = {'NonPayType': 'Способ оплаты не выбран!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    data = {'error': error, 'basket': request.session["_basket_"]}
    return render(request, "pay_type.html", context=data)


def verification_5(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    user_type_pay = request.GET.get('payType')
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
    data = {'auth_triger': auth_triger, 'basket': request.session["_basket_"]}
    return render(request, "delivery.html", context=data)
