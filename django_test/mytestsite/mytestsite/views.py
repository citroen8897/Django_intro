from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import re
import time
import mysql.connector
from mysql.connector import Error
import hashlib
# import password_generator


def test_page(request):
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request, "test_page.html", context=data)


def hello(request):
    return render(request, "hello.html")


def page_1(request):
    data = {'login': request.GET.get('login')}
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
        user_password = generator_de_password(user_password)

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
        current_user = User(0, user_nom, user_prenom, user_login,
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
    if re.search(r"\w+\.*\w+@\w+\.\w+", request.GET.get('login')):
        user_login = request.GET.get('login')
    else:
        user_login = ''

    user_password = request.GET.get('password')
    if len(user_password) < 6:
        user_password = ''
    else:
        user_password = generator_de_password(user_password)

    if user_login != '' and user_password != '':
        current_user = User(0, 'user_nom', 'user_prenom', user_login,
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


def generator_de_password(string_input):
    temp_int = int((len(string_input) / 2))
    user_password_hash_1 = hashlib.md5(string_input[:temp_int].
                                       encode('utf-8')).hexdigest()
    index_i, index_j = 0, 0
    for i in user_password_hash_1:
        if i.isdigit() and int(i) > 1:
            index_i = user_password_hash_1.index(i)
            break
    user_password_hash_1 = user_password_hash_1[:index_i] + \
                           str(int(user_password_hash_1[index_i]) ** 3) + \
                           user_password_hash_1[index_i + 1:]

    user_password_hash_2 = hashlib.sha1(string_input[temp_int:].
                                        encode('utf-8')).hexdigest()
    for j in user_password_hash_2:
        if j.isdigit() and int(j) > 1:
            index_j = user_password_hash_2.index(j)
            break
    user_password_hash_2 = user_password_hash_2[:index_j] + \
                           str(int(user_password_hash_2[index_j]) ** 4) + \
                           user_password_hash_2[index_j + 1:]

    user_password = user_password_hash_1 + 'f2006i' + user_password_hash_2
    return user_password


class User:
    def __init__(self, user_id, nom, prenom, login, telephone, password,
                 status):
        self.user_id = user_id
        self.nom = nom
        self.prenom = prenom
        self.login = login
        self.telephone = telephone
        self.password = password
        self.status = status
        self.users_data_base = []

    def add_user_database(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')

            if conn.is_connected():
                new_user = "INSERT INTO ASK_market_users" \
                           "(email,telephone,password,nom,prenom," \
                           "status) VALUES(%s,%s,%s,%s,%s,%s)"
                cursor = conn.cursor()
                cursor.execute(new_user, (self.login, self.telephone,
                                          self.password, self.nom,
                                          self.prenom, self.status))
                if cursor.lastrowid:
                    print('успешно добавлена запись. id пользователя: ',
                          cursor.lastrowid)
                else:
                    print('какая-то ошибка...')

                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_users_db(self):
        try:
            conn = mysql.connector.connect(user='root',
                                           host='localhost',
                                           database='mysql')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ASK_market_users")
                row = cursor.fetchone()
                while row is not None:
                    self.users_data_base.append(User(row[0], row[4], row[5],
                                                     row[1], row[2], row[3],
                                                     row[6]))
                    row = cursor.fetchone()
                conn.commit()
        except Error as error:
            print(error)
        finally:
            conn.close()
            cursor.close()

    def get_current_user(self):
        for person in self.users_data_base:
            if self.login == person.login and self.password == person.password:
                self.user_id = person.user_id
                self.nom = person.nom
                self.prenom = person.prenom
                self.login = person.login
                self.password = person.password
                self.telephone = person.telephone
                self.status = person.status
