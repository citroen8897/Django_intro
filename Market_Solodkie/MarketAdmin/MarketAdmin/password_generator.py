import hashlib


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
