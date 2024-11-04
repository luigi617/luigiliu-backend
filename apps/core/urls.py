# urls.py

from django.urls import path
from .views import get_csrf_token

core_urlpatterns = [
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
]
