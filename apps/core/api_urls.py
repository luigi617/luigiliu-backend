from apps.user.urls import users_urlpatterns
from apps.article.urls import articles_urlpatterns
from apps.home.urls import home_urlpatterns
from apps.treasure_hunt.urls import treasure_hunt_urlpatterns
from apps.map.urls import map_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    users_urlpatterns +
    articles_urlpatterns +
    home_urlpatterns +
    treasure_hunt_urlpatterns +
    map_urlpatterns
)