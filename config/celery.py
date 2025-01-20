import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('luigiliu-backend')

# Load config from Django settings, the CELERY namespace means all Celery-related config
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks across all apps
app.autodiscover_tasks()
