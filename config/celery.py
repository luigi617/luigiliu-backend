import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('luigiliu-backend')

# Load config from Django settings, the CELERY namespace means all Celery-related config
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks across all apps
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'import_nba_standing': {
        'task': 'apps.nba.tasks.import_standing',
        'schedule': crontab(minute='*/5'),  # Every 4 hours
        'args': (),
    },
    'import_nba_games': {
        'task': 'apps.nba.tasks.import_games',
        'schedule': crontab(hour='*/4'),  # Every 4 hours
        'args': (),
    },
}