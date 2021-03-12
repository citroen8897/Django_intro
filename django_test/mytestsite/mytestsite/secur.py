def secur_x(string):
    for j in ['delete', 'insert', 'set', 'update', 'drop']:
        if j in string.lower():
            return 0
