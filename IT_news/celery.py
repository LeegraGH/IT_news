from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab  # scheduler

# настройки django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IT_news.settings')
app = Celery('IT_news')
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # выполняется каждую минуту
    'scraping-task-one-min': {
        'task': 'articles.tasks.habr_parse',
        'schedule': crontab(minute='*/1')  # Запуск каждую минуту
    }
}
