from __future__ import absolute_import , unicode_literals
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'car_service.settings')

app = Celery('car_service')

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Riyadh')

app.config_from_object(settings , namespace='CELERY')

# # Celery beat settings
# app.conf.beat_schedule = {
#     'send_mail_every_day':{
#         'task': 'send_mail_app.tasks.send_mail_func',
#         'schedule': crontab(minute=0),
#         #'args': (2,)
#     }
# }
app.autodiscover_tasks()

@app.task(bind=True)
def debug(self):
    print(f'Request: {self.request!r}')