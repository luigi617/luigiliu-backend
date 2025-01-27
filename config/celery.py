import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('luigiliu-backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'import_nba_standing': {
        'task': 'apps.nba.tasks.import_standing',
        'schedule': crontab(minute=0, hour='*/4'),  # Every 4 hours
        'args': (),
    },
    'import_nba_games': {
        'task': 'apps.nba.tasks.import_games',
        'schedule': crontab(minute=0, hour='*/4'),  # Every 4 hours
        'args': (),
    },
}