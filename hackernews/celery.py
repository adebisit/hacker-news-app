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


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

