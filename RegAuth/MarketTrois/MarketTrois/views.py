from django.shortcuts import redirect
from django.shortcuts import render
import re
from . import password_generator
from . import secur
from .forms import AuthForm, RegForm, CategoryForm
import requests
import datetime


def authorization(request):
    auth_form = AuthForm()
    if request.method == 'POST':
        if secur.secur_x(str(request.POST)) == 0:
            return redirect('https://football.kulichki.net/')
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            user_login = auth_form.cleaned_data["login"]
            user_password = auth_form.cleaned_data["password"]
            if re.search(r"\w+\.*\w+@\w+\.\w+", user_login):
                user_login = user_login
            else:
                user_login = ''
            if len(user_password) < 6:
                user_password = ''
            else:
                user_password = password_generator.generator_de_password(
                    user_password)
            if user_login != '' and user_password != '':
                response = requests.get('http://127.0.0.1:8000/api/user/')
                users_data_base = response.json()
                current_user = ''
                for user in users_data_base:
                    if user['login'] == user_login and \
                            user['password'] == user_password:
                        current_user = user
                if current_user != '':
                    request.session["user_id"] = current_user['id']
                    request.session["login"] = current_user['login']
                    request.session["password"] = current_user['password']
                    return redirect('/account')
                else:
                    data = {'auth_form': auth_form,
                            'user_error': 'Пользователь с такими данными не '
                                          'найден!'}
                    return render(request, "auth_telegram.html", context=data)
            else:
                data = {'auth_form': auth_form,
                        'user_error': 'корректно заполните поля!'}
                return render(request, "auth_telegram.html", context=data)
    data = {'auth_form': auth_form}
    return render(request, "auth_telegram.html", context=data)


def registration(request):
    reg_form = RegForm()
    if request.method == 'POST':
        if secur.secur_x(str(request.POST)) == 0:
            return redirect('https://football.kulichki.net/')
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            user_login = reg_form.cleaned_data["login"]
            user_password = reg_form.cleaned_data["password"]
            user_password_rep = reg_form.cleaned_data["password_rep"]
            user_nom = reg_form.cleaned_data["nom"]
            user_prenom = reg_form.cleaned_data["prenom"]
            user_telephone = reg_form.cleaned_data["telephone"]

            if re.search(r"\w+\.*\w+@\w+\.\w+", user_login):
                user_login = user_login
            else:
                user_login = ''

            for element in user_telephone:
                if not element.isdigit():
                    user_telephone = user_telephone.replace(element, "")
            if len(user_telephone) < 10:
                user_telephone = ''
            else:
                if not user_telephone.startswith("+38"):
                    user_telephone = "+38" + user_telephone[-10:]

            if user_password != user_password_rep or len(user_password) < 6:
                user_password = ''
            else:
                user_password = password_generator.generator_de_password(
                    user_password)

            user_nom = user_nom.title()
            for element in user_nom:
                if not element.isalpha():
                    user_nom = ''

            user_prenom = user_prenom.title()
            for element in user_prenom:
                if not element.isalpha():
                    user_prenom = ''

            if user_login != '' and user_password != '' \
                    and user_telephone != '' and user_nom != '' \
                    and user_prenom != '':
                response = requests.get('http://127.0.0.1:8000/api/user/')
                users_data_base = response.json()
                unique_user = 1
                for user in users_data_base:
                    if user['login'] == user_login or \
                            user['telephone'] == user_telephone:
                        unique_user = 0
                if unique_user == 1:
                    post_data = {'login': user_login,
                                 'password': user_password,
                                 'nom': user_nom,
                                 'prenom': user_prenom,
                                 'telephone': user_telephone}
                    response = requests.post('http://127.0.0.1:8000/api/user/',
                                             data=post_data)
                    return redirect('/authorization')
                else:
                    data = {'reg_form': reg_form,
                            'user_error': 'e-mail или телефон уже '
                                          'зарегистрирован!'}
                    return render(request, "reg_telegram.html", context=data)
            else:
                data = {'reg_form': reg_form, 'user_error': 'корректно '
                                                            'заполните поля!'}
                return render(request, "reg_telegram.html", context=data)
    data = {'reg_form': reg_form}
    return render(request, "reg_telegram.html", context=data)


def account(request):
    helper_3 = 0
    if request.GET.get('helper_3'):
        helper_3 = int(request.GET.get('helper_3'))

    current_user_login = request.session["login"]
    current_user_password = request.session["password"]
    response = requests.get('http://127.0.0.1:8000/api/user/')
    users_data_base = response.json()
    for user in users_data_base:
        if user['login'] == current_user_login and \
                user['password'] == current_user_password:
            current_user = user

    response = requests.get('http://127.0.0.1:8000/api/category/')
    categories_data_base = response.json()
    request.session["categories"] = [j['nom'] for j in categories_data_base]

    response = requests.get('http://127.0.0.1:8000/api/product/')
    products_data_base = response.json()

    if request.GET.get('product_sort'):
        if request.GET.get('product_sort') == '0':
            products_data_base.sort(key=lambda j: j['id'])
        elif request.GET.get('product_sort') == '1':
            products_data_base.sort(key=lambda j: j['nom'])
        elif request.GET.get('product_sort') == '3':
            products_data_base.sort(key=lambda j: j['prix'])
        elif request.GET.get('product_sort') == '4':
            products_data_base.sort(key=lambda j: j['category'])
        elif request.GET.get('product_sort') == '5':
            products_data_base.sort(key=lambda j: j['etre'])
        elif request.GET.get('product_sort') == '7':
            products_data_base.sort(key=lambda j: j['author'])
        elif request.GET.get('product_sort') == '8':
            products_data_base.sort(key=lambda j: j['published_date'])
        elif request.GET.get('product_sort') == '9':
            products_data_base.sort(key=lambda j: j['modified_date'])
    data = {'helper_3': helper_3, 'users_data_base': users_data_base,
            'categories_data_base': categories_data_base,
            'products_data_base': products_data_base}
    return render(request, 'account_telegram.html', context=data)


def log_out(request):
    request.session.clear()
    return redirect('/authorization')


def add_product(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    error_dict = {'product_nom': 'Некорректное название!',
                  'product_quantity': 'Некорректная единица товара!',
                  'product_prix': 'Некорректная цена!',
                  'product_img': 'Некорректное изображение!',
                  'product_status': 'Некорректный статус!',
                  'product_category': 'Некорректная категория!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    categories_list = request.session["categories"]
    categories_list_mod = []
    for element in categories_list:
        categories_list_mod.append({
            'cat': [categories_list.index(element), element]})
    data = {'error': error, 'categories': categories_list_mod}
    return render(request, "add_product.html", context=data)


def verification_product(request):
    if request.POST:
        if secur.secur_x(str(request.POST)) == 0:
            return redirect('https://football.kulichki.net/')

    product_nom = request.POST.get('nom')
    if len(product_nom) == 0:
        product_nom = ''

    product_quantity = request.POST.get('quantity')
    if len(product_quantity) == 0:
        product_quantity = ''

    product_prix = request.POST.get('prix')
    if re.findall(r'[^0-9.]', str(product_prix)) or len(product_prix) == 0:
        product_prix = ''
    else:
        product_prix = float(product_prix)

    response = requests.get('http://127.0.0.1:8000/api/product/')
    products_data_base = response.json()
    author = request.session["login"]

    if len(products_data_base) > 0:
        last_product_id = products_data_base[-1]['id']
    else:
        last_product_id = 0
    if not request.FILES:
        product_img = ''
    else:
        product_img = request.FILES['productImg']
        product_img.name = str(last_product_id + 1)
        with open('MarketTrois/static/images/' + product_img.name, 'wb+') as \
                destination:
            for chunk in request.FILES['productImg'].chunks():
                destination.write(chunk)

    product_etre = request.POST.get('etre')
    if product_etre not in ['0', '1', '2', '3', '4']:
        product_etre = ''
    else:
        status_dict = {'0': 'в наличии', '1': 'нет в наличии',
                       '2': 'ожидается',
                       '3': 'под заказ', '4': 'снят с производства'}
        for k, v in status_dict.items():
            if k == product_etre:
                product_etre = v

    product_category = request.POST.get('category')
    categories_list = request.session["categories"]
    categories_dict = {}
    i = 0
    for j in categories_list:
        categories_dict[str(i)] = j
        i += 1
    for k, v in categories_dict.items():
        if k == product_category:
            product_category = v

    if product_nom != '' and product_quantity != '' and \
            product_prix != '' and product_img != '' and product_etre != ''\
            and product_category != '':
        post_data = {'nom': product_nom.title(),
                     'quantity': product_quantity,
                     'prix': product_prix,
                     'img': product_img.name,
                     'category': product_category,
                     'etre': product_etre,
                     'author': author}
        response = requests.post('http://127.0.0.1:8000/api/product/',
                                 data=post_data)
        data = {'error': 'Изменения сохранены'}
        return render(request, "account_telegram.html", context=data)
    else:
        temp = {'product_nom': product_nom,
                'product_quantity': product_quantity,
                'product_prix': product_prix,
                'product_img': product_img, 'product_status': product_etre}
        for k, v in temp.items():
            if v == '':
                return redirect(f'/add_product?error={k}')


def nouveau_category(request):
    category_form = CategoryForm()
    error = ''
    if request.method == 'POST':
        if secur.secur_x(str(request.POST)) == 0:
            return redirect('https://football.kulichki.net/')
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            nouveau_category = category_form.cleaned_data["nom"]
            if len(nouveau_category) == 0:
                nouveau_category = ''
            categories_list = request.session["categories"]

            if nouveau_category != '' and \
                    nouveau_category.title() not in categories_list:
                author = request.session["login"]
                post_data = {'nom': nouveau_category.title(),
                             'author': author}
                response = requests.post('http://127.0.0.1:8000/api/category/',
                                         data=post_data)
                data = {'error': 'Изменения сохранены'}
                return render(request, "account_telegram.html", context=data)
            else:
                error = 'Некорректно или дубликат категории!'

    data = {'cat_form': category_form, 'error': error}
    return render(request, "add_category.html", context=data)


def category_card(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    category_nom = request.GET.get('category_nom')
    request.session["category_nom"] = category_nom
    data = {'category_nom': category_nom}
    return render(request, "category_card.html", context=data)


def chansir_category_nom(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    categories_list = request.session["categories"]
    if len(request.GET.get('nom')) != 0 and \
            (request.GET.get('nom')).title() not in categories_list:
        category_nom_nouveau = request.GET.get('nom')
        category_nom_old = request.session["category_nom"]
        response = requests.get('http://127.0.0.1:8000/api/category/')
        categories_data_base = response.json()
        for j in categories_data_base:
            if j['nom'] == category_nom_old:
                author = request.session["login"]
                post_data = {'nom': category_nom_nouveau.title(),
                             'author': author,
                             'modified_date': datetime.datetime.now()}
                response = requests.put(
                    f'http://127.0.0.1:8000/api/category/{j["id"]}',
                    data=post_data)
        response = requests.get('http://127.0.0.1:8000/api/product/')
        products_data_base = response.json()
        for i in products_data_base:
            if i['category'] == category_nom_old:
                author = request.session["login"]
                post_data = {'category': category_nom_nouveau.title(),
                             'author': author,
                             'modified_date': datetime.datetime.now(),
                             'nom': i["nom"],
                             'quantity': i["quantity"],
                             'prix': i["prix"],
                             'img': i["img"],
                             'etre': i["etre"]}
                response = requests.put(
                    f'http://127.0.0.1:8000/api/product/{i["id"]}',
                    data=post_data)
        data = {'error': 'Изменения сохранены'}
        return render(request, "account_telegram.html", context=data)
    else:
        data = {'error': 'Некорректно или дубликат! Изменения не сохранены!'}
        return render(request, "account_telegram.html", context=data)


def delete_category(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    category_nom = request.session["category_nom"]
    response = requests.get('http://127.0.0.1:8000/api/category/')
    categories_data_base = response.json()
    for j in categories_data_base:
        if j['nom'] == category_nom:
            response = requests.delete(
                f'http://127.0.0.1:8000/api/category/{j["id"]}')
    response = requests.get('http://127.0.0.1:8000/api/product/')
    products_data_base = response.json()
    for i in products_data_base:
        if i['category'] == category_nom:
            response = requests.delete(
                f'http://127.0.0.1:8000/api/product/{i["id"]}')
    data = {'error': 'Изменения сохранены'}
    return render(request, "account_telegram.html", context=data)


def product_card(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.GET.get('product_id')
    request.session["product_id"] = product_id
    response = requests.get('http://127.0.0.1:8000/api/product/')
    products_data_base = response.json()
    for product in products_data_base:
        if product['id'] == int(product_id):
            current_product = product
    categories_list = request.session["categories"]
    categories_list_mod = []
    for element in categories_list:
        categories_list_mod.append({
            'cat': [categories_list.index(element), element]})
    data = {'categories': categories_list_mod,
            'current_product': current_product}
    return render(request, "product_card.html", context=data)


def verification_product_card(request):
    if request.POST:
        if secur.secur_x(str(request.POST)) == 0:
            return redirect('https://football.kulichki.net/')

    product_id = request.session["product_id"]
    response = requests.get('http://127.0.0.1:8000/api/product/')
    products_data_base = response.json()
    for product in products_data_base:
        if product['id'] == int(product_id):
            current_product = product

    product_nom = request.POST.get('nom')
    if len(product_nom) == 0:
        product_nom = ''

    product_quantity = request.POST.get('quantity')
    if len(product_quantity) == 0:
        product_quantity = ''

    product_prix = request.POST.get('prix')
    if re.findall(r'[^0-9.]', str(product_prix)) or len(product_prix) == 0:
        product_prix = ''
    else:
        product_prix = float(product_prix)

    if not request.FILES:
        product_img = ''
    else:
        product_img = request.FILES['productImg']
        product_img.name = current_product['img']
        with open('MarketTrois/static/images/' + product_img.name, 'wb+') as \
                destination:
            for chunk in request.FILES['productImg'].chunks():
                destination.write(chunk)

        author = request.session["login"]
        post_data = {'category': current_product['category'],
                     'author': author,
                     'modified_date': datetime.datetime.now(),
                     'nom': current_product['nom'],
                     'quantity': current_product['quantity'],
                     'prix': current_product['prix'],
                     'img': product_img.name,
                     'etre': current_product['etre']}
        response = requests.put(
            f'http://127.0.0.1:8000/api/product/{current_product["id"]}',
            data=post_data)

    product_etre = request.POST.get('etre')
    if product_etre not in ['0', '1', '2', '3', '4']:
        product_etre = ''
    else:
        status_dict = {'0': 'в наличии', '1': 'нет в наличии',
                       '2': 'ожидается',
                       '3': 'под заказ', '4': 'снят с производства'}
        for k, v in status_dict.items():
            if k == product_etre:
                product_etre = v

    product_category = request.POST.get('category')
    categories_list = request.session["categories"]
    categories_dict = {}
    i = 0
    for j in categories_list:
        categories_dict[str(i)] = j
        i += 1
    for k, v in categories_dict.items():
        if k == product_category:
            product_category = v

    for product in products_data_base:
        if product['id'] == int(product_id):
            current_product = product
    author = request.session["login"]
    post_data = {'category': current_product['category'],
                 'author': author,
                 'modified_date': datetime.datetime.now(),
                 'nom': current_product['nom'],
                 'quantity': current_product['quantity'],
                 'prix': current_product['prix'],
                 'img': current_product['img'],
                 'etre': current_product['etre']}

    if product_nom != '':
        post_data['nom'] = product_nom

    if product_quantity != '':
        post_data['quantity'] = product_quantity

    if product_prix != '':
        post_data['prix'] = product_prix

    if product_etre != '':
        post_data['etre'] = product_etre

    if product_category != '':
        post_data['category'] = product_category

    response = requests.put(
        f'http://127.0.0.1:8000/api/product/{current_product["id"]}',
        data=post_data)
    data = {'error': 'Изменения сохранены'}
    return render(request, "account_telegram.html", context=data)


def delete_product(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    product_id = request.session["product_id"]
    response = requests.get('http://127.0.0.1:8000/api/product/')
    products_data_base = response.json()
    for product in products_data_base:
        if product['id'] == int(product_id):
            current_product = product

    response = requests.delete(
        f'http://127.0.0.1:8000/api/product/{current_product["id"]}')
    data = {'error': 'Изменения сохранены'}
    return render(request, "account_telegram.html", context=data)


def verification_chercher(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')
    admin_search = request.GET.get('admin_search')
    response = requests.get('http://127.0.0.1:8000/api/product/')
    product_chercher = response.json()
    product_chercher_mod = []
    for e in product_chercher:
        if admin_search in str(e['id']):
            product_chercher_mod.append(e)
        if admin_search.lower() in e['nom'].lower() or \
                e['nom'].lower() in admin_search.lower():
            if e not in product_chercher_mod:
                product_chercher_mod.append(e)
        if admin_search.lower() in e['category'].lower() or \
                e['category'].lower() in admin_search.lower():
            if e not in product_chercher_mod:
                product_chercher_mod.append(e)
        if admin_search.lower() in e['author'].lower():
            if e not in product_chercher_mod:
                product_chercher_mod.append(e)

    data = {'product_chercher': product_chercher_mod,
            'error': 'По запросу ничего не найдено!'}
    return render(request, "chercher_result.html", context=data)
