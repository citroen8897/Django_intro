from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import re
from . import password_generator
from . import secur
from .forms import AuthForm, RegForm
from . import user_telegram


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
                                                      'user_nom', 'user_prenom')
                new_user.get_users_db()
                new_user.get_current_user()
                if new_user.user_id != 0:
                    return redirect('/account_solodkie')
                else:
                    data = {'auth_form': auth_form,
                            'user_error': 'Пользователь с такими данными не найден!'}
                    return render(request, "auth_telegram.html", context=data)
            else:
                data = {'auth_form': auth_form, 'user_error': 'корректно заполните поля!'}
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
                                                      user_nom, user_prenom)
                new_user.get_users_db()
                if new_user.login not in \
                        [element.login for element in
                         new_user.users_data_base] \
                        and new_user.telephone not in \
                        [element.telephone for element in
                         new_user.users_data_base]:
                    new_user.add_user_data_base()
                    return redirect('/authorization_solodkie')
                else:
                    data = {'reg_form': reg_form,
                            'user_error': 'e-mail или телефон уже зарегистрирован!'}
                    return render(request, "reg_telegram.html", context=data)
            else:
                data = {'reg_form': reg_form, 'user_error': 'корректно заполните поля!'}
                return render(request, "reg_telegram.html", context=data)
    data = {'reg_form': reg_form}
    return render(request, "reg_telegram.html", context=data)


def account_solodkie(request):
    return render(request, 'account_telegram.html')
