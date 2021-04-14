import telebot
import json
import re
import datetime
from telebot import types
import sqlite3

bot = telebot.TeleBot("1515003198:AAFoLiPvifdpb1wGk1i62MZWeLW6cZdV8cE")
owner = 434385416
julia = 1160338498
predator = 572889721
# file_data_base = open("data_base_des_elements_v3.json", "r")
# list_menu = json.load(file_data_base)
# file_data_base.close()

products_data_base = []
try:
    sqlite_connection = sqlite3.connect('db.sqlite3')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
    cursor.execute("SELECT * FROM admin_tele_magaz_producttelegramtable")
    one_result = cursor.fetchone()
    while one_result is not None:
        products_data_base.append([one_result[0], one_result[1],
                                   one_result[2], one_result[3],
                                   one_result[4], one_result[5],
                                   one_result[6]])
        one_result = cursor.fetchone()

except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
print(products_data_base)

list_menu = [[products_data_base[0][4]]]
for j in products_data_base:
    if j[4] not in [r[0] for r in list_menu]:
        list_menu.append([j[4]])
print(list_menu)
for j in products_data_base:
    for i in list_menu:
        if j[4] in i:
            i.append([j[1], j[2], j[3], j[5], j[6], j[0]])
print(list_menu)


def get_jour_de_envoyer():
    jours_dict = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7,
    }
    ajourdhui = datetime.datetime.today().strftime("%A")
    temps_maintenant_heure = int(datetime.datetime.today().strftime("%H"))

    if ajourdhui in ("Tuesday", "Wednesday"):
        jour_de_envoyer = "Воскресенье"
        jour_key = "Sunday"
    elif ajourdhui == "Monday" and temps_maintenant_heure > 20:
        jour_de_envoyer = "Воскресенье"
        jour_key = "Sunday"
    elif ajourdhui == "Thursday" and temps_maintenant_heure < 20:
        jour_de_envoyer = "Воскресенье"
        jour_key = "Sunday"
    else:
        jour_de_envoyer = "Четверг"
        jour_key = "Thursday"

    if jour_key == "Sunday":
        delta_jour = jours_dict[f"{jour_key}"] - jours_dict[f"{ajourdhui}"]
        temp_delta = datetime.timedelta(days=delta_jour)
        envoyer_date = (datetime.datetime.today() + temp_delta).strftime(
            "%d.%m"
        )

    elif jour_key == "Thursday" and ajourdhui != "Monday":
        delta_jour = 7 - (
            jours_dict[f"{ajourdhui}"] - jours_dict[f"{jour_key}"]
        )
        temp_delta = datetime.timedelta(days=delta_jour)
        envoyer_date = (datetime.datetime.today() + temp_delta).strftime(
            "%d.%m"
        )

    else:
        delta_jour = jours_dict[f"{jour_key}"] - jours_dict[f"{ajourdhui}"]
        temp_delta = datetime.timedelta(days=delta_jour)
        envoyer_date = (datetime.datetime.today() + temp_delta).strftime(
            "%d.%m"
        )

    return jour_de_envoyer, envoyer_date


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Каталог")
    btn2 = types.KeyboardButton("Корзина")
    btn3 = types.KeyboardButton("Контакты")
    btn4 = types.KeyboardButton("О нас")
    btn5 = types.KeyboardButton("Доставка")
    btn6 = types.KeyboardButton("Оплата")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    send_mess = (
        f"Привет {message.from_user.first_name} "
        f"{message.from_user.last_name}"
    )
    bot.send_message(message.chat.id, send_mess, reply_markup=markup)

    user_file = open(f"{message.from_user.id}.json", "w")
    user_basket = []
    user_info = {}
    user = {"basket": user_basket, "info": user_info, "changir": 1}
    data_pour_ecrire = json.dumps(user, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()


@bot.message_handler(content_types=["text"])
def step_un(message):
    un_repondre = message.text
    if un_repondre == "Каталог":
        catalogue(message)
    elif un_repondre == "Корзина":
        get_basket(message)
    elif un_repondre == "Контакты":
        contacts(message)
    elif un_repondre == "О нас":
        pour_nous(message)
    elif un_repondre == "Доставка":
        delivery_info_total(message)
    elif un_repondre == "Оплата":
        acheter_info(message)
    else:
        return start


@bot.message_handler(content_types=["text"])
def catalogue(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()
    user_file_data["changir"] = 1
    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button_list = []
    for t in list_menu:
        callback_button_list.append(types.InlineKeyboardButton(
            text=t[0], callback_data=(list_menu.index(t) + 1000)))
    for t in callback_button_list:
        keyboard.add(t)
    bot.send_message(
        message.chat.id, "Категории товаров:", reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)

    if int(call.data) in range(1000, 1100):
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard_2 = types.InlineKeyboardMarkup(row_width=1)
        callback_button_list = []
        for t in list_menu[int(call.data) - 1000][1:]:
            callback_button_list.append(types.InlineKeyboardButton(
                text=t[0], callback_data=t[5]))
        for t in callback_button_list:
            keyboard_2.add(t)
        bot.send_message(
            call.message.chat.id, "Товары в данной категории:",
            reply_markup=keyboard_2
        )

    elif int(call.data) in range(500):
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)

        current_product_numero = int(call.data)
        for element in list_menu:
            for w in element[1:]:
                if w[5] == current_product_numero:
                    current_product = w

        temp_acheter = {
            "название": current_product[0],
            "количество": current_product[1],
            "стоимость": current_product[2],
            "кол-во": 1,
        }
        temp_file = open(f"{call.message.chat.id}temp.json", "w")
        data_pour_ecrire = json.dumps(temp_acheter, indent=4)
        temp_file.write(data_pour_ecrire)
        temp_file.close()

        bot.send_photo(
            call.message.chat.id,
            open(f'MarketAdmin/static/images/{current_product[4]}', "rb"),
        )
        msg = (
            f"{current_product[0]}\n"
            f'{current_product[3]}\n'
            f'единица товара: {current_product[1]}\n'
            f'цена за единицу: {current_product[2]} грн.\n'
        )
        ajouter_a_basket(call.message, msg)

    elif call.data == "501":
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)
        ajouter_a_basket_2(call.message)

    elif call.data == "502":
        temp_file = open(f"{call.message.chat.id}temp.json", "r")
        temp_acheter = json.load(temp_file)
        temp_file.close()
        temp_acheter["кол-во"] += 1
        temp_file = open(f"{call.message.chat.id}temp.json", "w")
        data_pour_ecrire = json.dumps(temp_acheter, indent=4)
        temp_file.write(data_pour_ecrire)
        temp_file.close()
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)
        ajouter_a_basket_2(call.message)

    elif call.data == "503":
        temp_file = open(f"{call.message.chat.id}temp.json", "r")
        temp_acheter = json.load(temp_file)
        temp_file.close()
        if temp_acheter["кол-во"] != 1:
            temp_acheter["кол-во"] -= 1
            temp_file = open(f"{call.message.chat.id}temp.json", "w")
            data_pour_ecrire = json.dumps(temp_acheter, indent=4)
            temp_file.write(data_pour_ecrire)
            temp_file.close()
            bot.edit_message_reply_markup(
                call.message.chat.id, call.message.message_id
            )
            bot.delete_message(call.message.chat.id, call.message.message_id)
            ajouter_a_basket_2(call.message)

    elif call.data == "504":
        user_file = open(f"{call.message.chat.id}.json", "r")
        user_file_data = json.load(user_file)
        user_file.close()
        temp_file = open(f"{call.message.chat.id}temp.json", "r")
        temp_acheter = json.load(temp_file)
        temp_file.close()
        user_file_data["basket"].append(temp_acheter)
        user_file = open(f"{call.message.chat.id}.json", "w")
        data_pour_ecrire = json.dumps(user_file_data, indent=4)
        user_file.write(data_pour_ecrire)
        user_file.close()
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Товар добавлен в корзину")

        # if user_file_data["changir"] == 1:
        #     items_temp = []
        #     for j in range(len(list_menu)):
        #         element = list_menu[j]
        #         for k, v in element.items():
        #             items_temp.append([k, v])
        #     for element in items_temp:
        #         if temp_acheter["название"] in element[1].keys():
        #             temp_x_index_ = items_temp.index(element) + 1
        #             nom_de_catalogue_appeller = (
        #                 f"catalogue_{str(temp_x_index_)}(call.message)"
        #             )
        #             eval(nom_de_catalogue_appeller)

    elif call.data == "505":
        user_file = open(f"{call.message.chat.id}.json", "r")
        user_file_data = json.load(user_file)
        user_file.close()
        temp_file = open(f"{call.message.chat.id}temp.json", "r")
        temp_acheter = json.load(temp_file)
        temp_file.close()
        temp_file = open(f"{call.message.chat.id}temp.json", "w")
        temp_file.close()
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Товар удален из корзины")

        # if user_file_data["changir"] == 1:
        #     items_temp = []
        #     for j in range(len(list_menu)):
        #         element = list_menu[j]
        #         for k, v in element.items():
        #             items_temp.append([k, v])
        #     for element in items_temp:
        #         if temp_acheter["название"] in element[1].keys():
        #             temp_x_index_ = items_temp.index(element) + 1
        #             nom_de_catalogue_appeller = (
        #                 f"catalogue_{str(temp_x_index_)}(call.message)"
        #             )
        #             eval(nom_de_catalogue_appeller)

    elif call.data == "601":
        modifer_basket(call.message)

    elif call.data == "602":
        finir_1(call.message)

    elif call.data == "701":
        user_file = open(f"{call.message.chat.id}.json", "r")
        user_file_data = json.load(user_file)
        user_file.close()

        user_file_data["info"]["delivery_type"] = "Адресная доставка"

        user_file = open(f"{call.message.chat.id}.json", "w")
        data_pour_ecrire = json.dumps(user_file_data, indent=4)
        user_file.write(data_pour_ecrire)
        user_file.close()

        msg = bot.send_message(
            call.message.chat.id,
            "Укажите детали " "доставки\n" "/Город, адрес доставки/",
        )
        bot.register_next_step_handler(msg, get_delivery_info)

    elif call.data == "702":
        user_file = open(f"{call.message.chat.id}.json", "r")
        user_file_data = json.load(user_file)
        user_file.close()

        user_file_data["info"]["delivery_type"] = "Почтомат Новой Почты"

        user_file = open(f"{call.message.chat.id}.json", "w")
        data_pour_ecrire = json.dumps(user_file_data, indent=4)
        user_file.write(data_pour_ecrire)
        user_file.close()

        msg = bot.send_message(
            call.message.chat.id,
            "Укажите детали " "доставки\n" "/Город, адрес/номер " "почтомата/",
        )
        bot.register_next_step_handler(msg, get_delivery_info)

    elif call.data == "703":
        user_file = open(f"{call.message.chat.id}.json", "r")
        user_file_data = json.load(user_file)
        user_file.close()

        user_file_data["info"]["delivery_type"] = "Почтомат MeestExpress"

        user_file = open(f"{call.message.chat.id}.json", "w")
        data_pour_ecrire = json.dumps(user_file_data, indent=4)
        user_file.write(data_pour_ecrire)
        user_file.close()

        msg = bot.send_message(
            call.message.chat.id,
            "Укажите детали " "доставки\n" "/Город, адрес/номер " "почтомата/",
        )
        bot.register_next_step_handler(msg, get_delivery_info)

    elif call.data == "704":
        user_file = open(f"{call.message.chat.id}.json", "r")
        user_file_data = json.load(user_file)
        user_file.close()

        user_file_data["info"]["delivery_type"] = "Отделение Новой Почты"

        user_file = open(f"{call.message.chat.id}.json", "w")
        data_pour_ecrire = json.dumps(user_file_data, indent=4)
        user_file.write(data_pour_ecrire)
        user_file.close()

        msg = bot.send_message(
            call.message.chat.id,
            "Укажите детали "
            "доставки\n"
            "/Город, номер "
            "отделения Новой Почты/",
        )
        bot.register_next_step_handler(msg, get_delivery_info)

    elif call.data == "705":
        user_file = open(f"{call.message.chat.id}.json", "r")
        user_file_data = json.load(user_file)
        user_file.close()

        user_file_data["info"]["delivery_type"] = "Отделение MeestExpress"

        user_file = open(f"{call.message.chat.id}.json", "w")
        data_pour_ecrire = json.dumps(user_file_data, indent=4)
        user_file.write(data_pour_ecrire)
        user_file.close()

        msg = bot.send_message(
            call.message.chat.id,
            "Укажите детали "
            "доставки\n"
            "/Город, номер отделения "
            "MeestExpress/",
        )
        bot.register_next_step_handler(msg, get_delivery_info)


@bot.message_handler(content_types=["text"])
def ajouter_a_basket(message, text):
    keyboard_2 = types.InlineKeyboardMarkup(row_width=1)
    callback_button_1 = types.InlineKeyboardButton(
        text="Добавить в корзину", callback_data=501
    )
    keyboard_2.add(callback_button_1)
    bot.send_message(message.chat.id, text, reply_markup=keyboard_2)


@bot.message_handler(content_types=["text"])
def ajouter_a_basket_2(message):
    keyboard_2 = types.InlineKeyboardMarkup(row_width=3)
    callback_button_1 = types.InlineKeyboardButton(text="+", callback_data=502)
    callback_button_2 = types.InlineKeyboardButton(text="-", callback_data=503)
    callback_button_3 = types.InlineKeyboardButton(
        text="подтвердить", callback_data=504
    )
    callback_button_4 = types.InlineKeyboardButton(
        text="удалить", callback_data=505
    )
    keyboard_2.add(
        callback_button_1,
        callback_button_2,
        callback_button_3,
        callback_button_4,
    )

    temp_file = open(f"{message.chat.id}temp.json", "r")
    temp_acheter = json.load(temp_file)
    temp_file.close()

    temp_prix = temp_acheter["кол-во"] * int(temp_acheter["стоимость"])
    msg = (
        f'Товар: {temp_acheter["название"]}\n'
        f'В единице товара: {temp_acheter["количество"]}\n'
        f'Стоимость единицы товара: {temp_acheter["стоимость"]} грн.\n'
        f'Количество: {temp_acheter["кол-во"]}\n'
        f"Итого за данный товар: {temp_prix} грн."
    )
    bot.send_message(message.chat.id, msg, reply_markup=keyboard_2)


@bot.message_handler(content_types=["text"])
def get_basket(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()
    if len(user_file_data["basket"]) == 0:
        bot.send_message(message.chat.id, "Корзина пуста:(")
    else:
        bot.send_message(message.chat.id, "Ваш заказ:")
        total_prix = 0
        numero = 1
        for i in user_file_data["basket"]:
            temp_prix_1 = i["кол-во"] * int(i["стоимость"])
            total_prix += temp_prix_1
            zakaz_info = (
                f'{numero}. {i["название"]} {i["количество"]} * '
                f'{i["кол-во"]} шт. = {temp_prix_1} грн.\n'
            )
            bot.send_message(message.chat.id, zakaz_info)
            numero += 1

        if total_prix < 700:
            adress_delivery_prix = 85
            msg = (
                f"{numero}. Адресная доставка - "
                f"{adress_delivery_prix} грн. (заказ меньше 700 грн.)"
            )
            bot.send_message(message.chat.id, msg)
            total_prix += adress_delivery_prix
        else:
            adress_delivery_prix = 0
            total_prix += adress_delivery_prix

        keyboard_2 = types.InlineKeyboardMarkup(row_width=1)
        callback_button_1 = types.InlineKeyboardButton(
            text="редактировать " "корзину", callback_data=601
        )
        callback_button_2 = types.InlineKeyboardButton(
            text="оформить заказ", callback_data=602
        )
        keyboard_2.add(callback_button_1, callback_button_2)

        bot.send_message(
            message.chat.id,
            f"Итого: {total_prix} грн.",
            reply_markup=keyboard_2,
        )


@bot.message_handler(content_types=["text"])
def modifer_basket(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()

    temp_file = open(f"{message.chat.id}temp.json", "w")
    data_pour_ecrire = json.dumps(user_file_data["basket"][0], indent=4)
    temp_file.write(data_pour_ecrire)
    temp_file.close()

    user_file_data["basket"].pop(0)
    user_file_data["changir"] = 0
    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()

    ajouter_a_basket_2(message)


@bot.message_handler(content_types=["text"])
def finir_1(message):

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(
        text="Отправить номер телефона", request_contact=True
    )
    keyboard.add(button_phone)
    bot.send_message(
        message.chat.id,
        "Разрешите доступ к номеру телефона",
        reply_markup=keyboard,
    )


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()

    user_file_data["info"]["telephone"] = message.contact.phone_number

    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Каталог")
    btn2 = types.KeyboardButton("Корзина")
    btn3 = types.KeyboardButton("Контакты")
    btn4 = types.KeyboardButton("О нас")
    btn5 = types.KeyboardButton("Доставка")
    btn6 = types.KeyboardButton("Оплата")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    send_mess = "Спасибо!"
    bot.send_message(message.chat.id, send_mess, reply_markup=markup)

    msg = bot.send_message(message.chat.id, "Напишите Ваш e-mail")
    bot.register_next_step_handler(msg, get_email)


@bot.message_handler(content_types=["text"])
def get_email(message):
    if not re.search(r"\w+\.*\w+@\w+\.\w{2,}", message.text):
        msg = bot.send_message(
            message.chat.id, "Некорректный адрес. " "Повторите..."
        )
        bot.register_next_step_handler(msg, get_email)
        return

    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()

    user_file_data["info"]["e-mail"] = message.text

    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()

    msg = bot.send_message(message.chat.id, "Напишите Вашу фамилию")
    bot.register_next_step_handler(msg, get_prenom)


@bot.message_handler(content_types=["text"])
def get_prenom(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()

    user_file_data["info"]["prenom"] = message.text

    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()

    msg = bot.send_message(message.chat.id, "Напишите Ваше имя")
    bot.register_next_step_handler(msg, get_nom)


@bot.message_handler(content_types=["text"])
def get_nom(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()

    user_file_data["info"]["nom"] = message.text

    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()

    get_delivery_type(message)


@bot.message_handler(content_types=["text"])
def get_delivery_type(message):
    keyboard_2 = types.InlineKeyboardMarkup(row_width=1)
    callback_button_1 = types.InlineKeyboardButton(
        text="Адресная доставка", callback_data=701
    )
    callback_button_2 = types.InlineKeyboardButton(
        text="Почтомат Новая Почта", callback_data=702
    )
    callback_button_3 = types.InlineKeyboardButton(
        text="Почтомат MeestExpress", callback_data=703
    )
    callback_button_4 = types.InlineKeyboardButton(
        text="Отделение Новой Почты", callback_data=704
    )
    callback_button_5 = types.InlineKeyboardButton(
        text="Отделение MeestExpress", callback_data=705
    )
    keyboard_2.add(
        callback_button_1,
        callback_button_2,
        callback_button_3,
        callback_button_4,
        callback_button_5,
    )
    bot.send_message(
        message.chat.id, "Выберите способ доставки", reply_markup=keyboard_2
    )


@bot.message_handler(content_types=["text"])
def get_delivery_info(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()

    user_file_data["info"]["delivery_info"] = message.text

    a, b = get_jour_de_envoyer()
    user_file_data["info"]["delivery_jour"] = a
    user_file_data["info"]["delivery_date"] = b

    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()
    bot.send_message(
        message.chat.id,
        "Заказ успешно оформлен!\n"
        "С Вами свяжется наш специалист"
        " для уточнения заказа.",
    )
    envoyer_cours_owner(message)


@bot.message_handler(content_types=["text"])
def envoyer_cours_owner(message):
    user_file = open(f"{message.chat.id}.json", "r")
    user_file_data = json.load(user_file)
    user_file.close()
    total_prix = 0
    numero = 1
    tout_des_pieces = "Новый заказ!\n\nТовар:\n"
    for i in user_file_data["basket"]:
        temp_prix_1 = i["кол-во"] * int(i["стоимость"])
        total_prix += temp_prix_1
        zakaz_info = (
            f'{numero}. {i["название"]} {i["количество"]} * '
            f'{i["кол-во"]} шт. = {temp_prix_1} грн.\n'
        )
        tout_des_pieces += str(zakaz_info)
        numero += 1
    tout_des_pieces += f"Итого: {total_prix} грн.\n\nДетали доставки:\n"
    delivery_info = (
        f'Телефон: {user_file_data["info"]["telephone"]}\n'
        f'E-mail: {user_file_data["info"]["e-mail"]}\n'
        f'Фамилия: {user_file_data["info"]["prenom"]}\n'
        f'Имя: {user_file_data["info"]["nom"]}\n'
        f"Способ доставки: "
        f'{user_file_data["info"]["delivery_type"]}\n'
        f"Адрес доставки: "
        f'{user_file_data["info"]["delivery_info"]}\n'
        f"День доставки: "
        f'{user_file_data["info"]["delivery_jour"]}\n'
        f"Дата доставки: "
        f'{user_file_data["info"]["delivery_date"]}\n'
    )
    tout_des_pieces += delivery_info
    bot.send_message(owner, tout_des_pieces)
    bot.send_message(julia, tout_des_pieces)
    bot.send_message(predator, tout_des_pieces)
    user_file_data["basket"].clear()
    user_file = open(f"{message.chat.id}.json", "w")
    data_pour_ecrire = json.dumps(user_file_data, indent=4)
    user_file.write(data_pour_ecrire)
    user_file.close()


@bot.message_handler(content_types=["text"])
def contacts(message):

    bot.send_message(
        message.chat.id,
        "Для связи с нами:\n\n"
        "Telegram-диспетчер - 066-043-24-97, "
        "Елена\n"
        "Администратор Маркета - 050-446-77-99 "
        "Юлия\n"
        "Основатели Маркета:\n"
        "067-504-01-13, Юлия Солодкая\n"
        "067-507-66-70, Руслан Солодкий",
    )


@bot.message_handler(content_types=["text"])
def pour_nous(message):
    bot.send_message(
        message.chat.id,
        "Вы зашли в Маркет Солодких, "
        "в котором можете приобрести продукты "
        "под заказ. Мы объединили мощности "
        "разных производств, что бы собрать "
        "для Вас уникальный пакет Milk "
        "Friends.\nСобственники Маркета - "
        "Руслан и Юлия Солодкие - производят "
        "молочный ассортимент, их "
        "друзья-производственники поставляют "
        "колбасные и кондитерские изделия, "
        "хлеб на закваске, соусы и джемы. "
        "А еще у нас есть самая вкусная "
        "красная икра и авторские украинские "
        "вина.\nУникальные продукты по "
        "приемлимым ценам к Вашему столу каждый "
        "день. Когда Вы уже не представляете "
        "вкусную жизнь без продуктов нашего "
        "Маркета, мы собираем для Вас Milk BOX "
        "- особенную коробку продуктов "
        "еженедельной доставки с глобальной "
        "скидкой, потому что мы производители и "
        "можем позволить это для друзей:)",
    )


@bot.message_handler(content_types=["text"])
def delivery_info_total(message):
    bot.send_message(
        message.chat.id,
        "Доставка\n\n"
        "Дни доставки - ЧЕТВЕРГ и ВОСКРЕСЕНЬЕ.\n"
        "Прием заказа на ЧЕТВЕРГ заканчивается в 20.00 "
        "ПОНЕДЕЛЬНИКА.\n"
        "Прием заказа на ВОСКРЕСЕНЬЕ заканчивается в 20.00 "
        "ЧЕТВЕРГА.\n"
        "Доставка пакета от 700 грн. БЕСПЛАТНАЯ "
        "(вино и икра не учитывается), до 700 грн., доставка "
        "85 грн.\nДоставка Новой Почтой и MeestExpress согласно "
        "тарифов перевозчика.",
    )


@bot.message_handler(content_types=["text"])
def acheter_info(message):
    bot.send_message(
        message.chat.id,
        "Оплата\n\nВ день доставки, Маркет готовит финальную "
        "накладную и отправляет ссылку клиенту на указанный "
        "номер телефона в Viber, Telegram для оплаты по "
        "фактическому весу продуктов в пакете клиента.\n"
        "Оплата на карту:\n"
        "Моно Банк 5375414101840014\n"
        "Приват 4731219611289525\n"
        "Солодкая Юлия Михайловна\n"
        "Учитывайте комиссию БАНКА.\n"
        "После оплаты присылайте скан на номер в Viber Админу "
        "Маркета Елене 0660432497.",
    )


if __name__ == "__main__":
    bot.polling()
