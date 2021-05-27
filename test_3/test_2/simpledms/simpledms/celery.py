from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpledms.settings')
app = Celery("simpledms")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(name="test_add_task")
def add(x, y):
    return x / y
