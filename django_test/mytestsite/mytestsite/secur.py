def secur_x(string):
    if string is not None:
        for r in string:
            if not r.isalpha():
                string = string.replace(r, '')
        for j in ['delete', 'insert', 'set', 'update', 'drop']:
            if j in string.lower():
                return 0
