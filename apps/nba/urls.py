# rl_agent/urls.py

from django.urls import path
from .views import GetGameList, GetStanding, LiveGameInformationSSE

nba_urlpatterns = [
    path("nba/games/", GetGameList.as_view(), name="nba-game-list"),
    path("nba/standing/", GetStanding.as_view(), name="nba-standing"),
    # path("nba/live-games/", LiveGameInformationSSE.as_view(), name="nba-live-game-list"),
]