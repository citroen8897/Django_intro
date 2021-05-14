import openpyxl

try:
    wb = openpyxl.load_workbook('архивы_реестр.xlsx')
    print(1)
except FileNotFoundError:
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet['A1'] = 'Название архива'
    sheet['B1'] = 'Дата формирования'
    sheet['C1'] = 'Кол-во док-тов в архиве'
    sheet['D1'] = 'Ссылка'
    wb.save(filename='архивы_реестр.xlsx')
    print(0)
