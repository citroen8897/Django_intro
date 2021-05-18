import openpyxl
import os
import shutil
from .models import Zip, Document
import datetime

ZIPS_REESTR_XLSX = './media/reestry/архивы_реестр.xlsx'
ZIPS_FOLDER = './media/zips/'
TODAY = datetime.datetime.today()
ZIP_NAME = TODAY.strftime("%d_%m_%Y")
FOLDER_DOCUMENTS = f'{ZIPS_FOLDER}/{ZIP_NAME}/Документи/'


def make_dir(folder_name, folder_path):
    path = os.path.join(folder_path, folder_name)
    os.mkdir(path)


def make_new_zip(request):
    date_start = request.POST.get('date_start')
    date_fin = request.POST.get('date_fin')

    make_dir(ZIP_NAME, ZIPS_FOLDER)

    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    sheet['A1'] = 'Регистрационный номер'
    sheet['B1'] = 'Дата создания'
    sheet['C1'] = 'Короткое описание'
    sheet['D1'] = 'Ссылка'

    make_dir('Документи', (ZIPS_FOLDER + ZIP_NAME))

    documents_data_base = Document.objects.filter(
        create_date__range=[date_start, date_fin])
    for document in documents_data_base:
        ## тут без коментарів - так не варто робити, ви потім на "продакшн" код не зустите
        doc_link = f'http://127.0.0.1:8000/documents/{document.id}'

        sheet.append([document.reg_number, document.create_date, document.comment, doc_link])
        wb.save(
            filename=f'{ZIPS_FOLDER}{ZIP_NAME}/Реестр_документов.xlsx')

        make_dir(document.reg_number, FOLDER_DOCUMENTS)

        shutil.copyfile(f"{document.main_file.file}",
                        f"{FOLDER_DOCUMENTS}{document.reg_number}/{document.main_file.name[9:]}")

    shutil.make_archive((ZIPS_FOLDER + ZIP_NAME), 'zip', (ZIPS_FOLDER + ZIP_NAME))
    shutil.rmtree(ZIPS_FOLDER + ZIP_NAME)

    Zip.objects.create(title_zip=ZIP_NAME, create_date_zip=TODAY,
                       quantity_docs=documents_data_base.count(),
                       link_zip='ХЗ',
                       date_start=date_start, date_fin=date_fin)
