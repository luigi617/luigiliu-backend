from apps.user.urls import users_urlpatterns
from apps.tictactoe.urls import tictactoe_urlpatterns
from apps.nba.urls import nba_urlpatterns
from apps.core.urls import core_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    core_urlpatterns + 
    users_urlpatterns +
    tictactoe_urlpatterns +
    nba_urlpatterns
)