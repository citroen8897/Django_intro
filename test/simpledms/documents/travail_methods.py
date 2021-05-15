import openpyxl


def zip_list_excel(zip_name, zip_date, zip_quantity_docs, zip_link):
    try:
        wb = openpyxl.load_workbook('./static/reestry/архивы_реестр.xlsx')
        sheet = wb['Sheet']

    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb['Sheet']
        sheet['A1'] = 'Название архива'
        sheet['B1'] = 'Дата формирования'
        sheet['C1'] = 'Кол-во док-тов в архиве'
        sheet['D1'] = 'Ссылка'

    finally:
        sheet.append([zip_name, zip_date, zip_quantity_docs, zip_link])
        wb.save(filename='./static/reestry/архивы_реестр.xlsx')
