import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings')


app = Celery(
    'hackernews',
    broker='redis://localhost:6379/1',
    backend='redis://localhost:6379'
)


app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'get-latest-news-items': {
        'task': 'news.tasks.get_history',
        'schedule': 300.0,
    },
    'get-latest-job-news-items': {
        'task': 'news.tasks.get_latest',
        'schedule': 300.0,
    }
}
app.conf.timezone = 'UTC'
