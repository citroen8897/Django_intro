import mysql.connector
from mysql.connector import Error


def get_all_biling():
    billing_list = []
    try:
        conn = mysql.connector.connect(user='root',
                                       host='localhost',
                                       database='mysql')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ASK_market_billing")
            row = cursor.fetchone()
            while row is not None:
                billing_list.append([row[1], row[4]])
                row = cursor.fetchone()
            conn.commit()
    except Error as error:
        print(error)
    finally:
        conn.close()
        cursor.close()

    temp_list = [billing_list[0]]
    for element in billing_list[1:]:
        if element[1] not in [i[1] for i in temp_list]:
            temp_list.append(element)
        else:
            for j in temp_list:
                if j[1] == element[1]:
                    j[0] += element[0]
    print(temp_list)
    billing_list = temp_list
    return billing_list


nouveau_billing = get_all_biling()


def refactor_users_table(nouveau_data):
    try:
        conn = mysql.connector.connect(user='root',
                                       host='localhost',
                                       database='mysql')

        if conn.is_connected():
            for j in nouveau_data:
                if 3000 < j[0] < 7000:
                    discount_ = 3
                elif 7000 < j[0] < 15000:
                    discount_ = 7
                elif 15000 < j[0]:
                    discount_ = 10
                elif j[0] < 3000:
                    discount_ = 0
                print(j[0], j[1], discount_)
                total_summ = f"UPDATE ASK_market_users SET " \
                             f"total_summ={j[0]} WHERE id={j[1]}"
                discount = f"UPDATE ASK_market_users SET " \
                           f"discount={discount_} WHERE id={j[1]}"
                cursor = conn.cursor()
                cursor.execute(total_summ)
                cursor.execute(discount)
                conn.commit()
    except Error as error:
        print(error)
    finally:
        conn.close()
        cursor.close()


refactor_users_table(nouveau_billing)
