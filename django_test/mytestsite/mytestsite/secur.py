def secur_x(string):
    if string is not None:
        if string.isalpha():
            for j in ['delete', 'insert', 'set', 'update', 'drop']:
                if j in string.lower():
                    return 0
