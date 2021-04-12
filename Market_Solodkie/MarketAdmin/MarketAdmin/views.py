from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import re
from . import password_generator
from . import secur
from .forms import AuthForm, RegForm
from . import user_telegram
from admin_tele_magaz.models import ProductCategoryTable
from admin_tele_magaz.models import ProductTelegramTable
from . import product_telegram


def authorization_solodkie(request):
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
                new_user = user_telegram.UserTelegram(0, user_login,
                                                      user_password,
                                                      'user_telephone',
                                                      'user_nom',
                                                      'user_prenom',
                                                      'reg_date')
                new_user.get_users_db()
                new_user.get_current_user()
                if new_user.user_id != 0:
                    request.session["user_id"] = new_user.user_id
                    request.session["login"] = new_user.login
                    request.session["password"] = new_user.password
                    return redirect('/account_solodkie')
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


def registration_solodkie(request):
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
                new_user = user_telegram.UserTelegram(0, user_login,
                                                      user_password,
                                                      user_telephone,
                                                      user_nom, user_prenom,
                                                      'reg_date')
                new_user.get_users_db()
                if new_user.login not in \
                        [element.login for element in
                         new_user.users_data_base] \
                        and new_user.telephone not in \
                        [element.telephone for element in
                         new_user.users_data_base]:
                    # new_user.add_user_data_base()
                    new_user.insert_user()
                    return redirect('/authorization_solodkie')
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


def account_solodkie(request):
    helper_3 = 0
    if request.GET.get('helper_3'):
        helper_3 = int(request.GET.get('helper_3'))
    current_user_login = request.session["login"]
    current_user_password = request.session["password"]
    current_user = user_telegram.UserTelegram(0, current_user_login,
                                              current_user_password,
                                              'telephone', 'nom', 'prenom',
                                              'reg_date')
    current_user.get_users_db()
    current_user.get_current_user()
    category_list = ProductCategoryTable.objects.all()
    request.session["categories"] = [z.nom for z in category_list]
    some_product = product_telegram.ProductTelegram(0, 'nom', 'etre', '0.0',
                                                    'kg', '0.0', 'img')
    some_product.get_products_db()
    data = {'helper_3': helper_3, 'current_user': current_user,
            'categories': category_list,
            'products_data_base': some_product.products_data_base}
    return render(request, 'account_telegram.html', context=data)


def log_out(request):
    request.session.clear()
    return redirect('/authorization_solodkie')


def add_product(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    error_dict = {'product_nom': 'Некорректное название!',
                  'product_quantity': 'Некорректная единица товара!',
                  'product_prix': 'Некорректная цена!',
                  'product_img': 'Некорректная ссылка!',
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

    some_product = product_telegram.ProductTelegram(0, 'nom', 'etre', '0.0',
                                                    'kg', '0.0', 'img')
    some_product.get_products_db()
    if len(some_product.products_data_base) > 0:
        last_product_id = some_product.products_data_base[::-1][0].id
    else:
        last_product_id = 0
    if not request.FILES['productImg']:
        product_img = ''
    else:
        product_img = request.FILES['productImg']
        product_img.name = str(last_product_id + 1)
        with open('MarketAdmin/static/images/' + product_img.name, 'wb+') as \
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
        nouveau_product = product_telegram.ProductTelegram(0, product_category,
                                                           product_nom,
                                                           product_etre,
                                                           product_quantity,
                                                           product_prix,
                                                           product_img)
        nouveau_product.add_product_db(request.session["login"])
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


def add_category(request):
    if request.GET:
        if secur.secur_x(str(request.GET)) == 0:
            return redirect('https://football.kulichki.net/')

    error_dict = {'category_nom': 'Некорректное или дублирующееся название!'}
    error = ''
    if request.GET.get('error'):
        error = request.GET.get('error')
        for k, v in error_dict.items():
            if k == error:
                error = v
    categories_list = request.session["categories"]
    data = {'error': error, 'categories': categories_list}
    return render(request, "add_category.html", context=data)


def verification_category(request):
    if request.POST:
        if secur.secur_x(str(request.POST)) == 0:
            return redirect('https://football.kulichki.net/')

    product_nom = request.POST.get('nom')
    if len(product_nom) == 0:
        product_nom = ''

    categories_list = request.session["categories"]
    if product_nom != '' and product_nom.title() not in categories_list:
        ProductCategoryTable.objects.create(nom=product_nom.title())
        data = {'error': 'Изменения сохранены'}
        return render(request, "account_telegram.html", context=data)
    else:
        return redirect('/add_category?error=category_nom')


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
        ProductCategoryTable.objects.filter(nom=category_nom_old).update(nom=category_nom_nouveau.title())
        ProductTelegramTable.objects.filter(category=category_nom_old).update(category=category_nom_nouveau.title())
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
    ProductCategoryTable.objects.filter(nom=category_nom).delete()
    ProductTelegramTable.objects.filter(category=category_nom).delete()
    data = {'error': 'Изменения сохранены'}
    return render(request, "account_telegram.html", context=data)
