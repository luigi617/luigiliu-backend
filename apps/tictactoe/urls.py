# rl_agent/urls.py

from django.urls import path
from .views import GetNextActionView

tictactoe_urlpatterns = [
    path('tic-tac-toe/get-next-action/', GetNextActionView.as_view(), name='get-next-action'),
]