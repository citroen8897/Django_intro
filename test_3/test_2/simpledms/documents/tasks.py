from celery import Celery
from celery.utils.log import get_task_logger
import os
from . import travail_methods

logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpledms.settings')
app = Celery("simpledms")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(name="make_new_zip_task")
def make_new_zip_task(date_start, date_fin, host):
    logger.info(f"Формирование архива документов c {date_start} по {date_fin}")
    print('В процессе....')
    return travail_methods.make_new_zip(date_start, date_fin, host)
