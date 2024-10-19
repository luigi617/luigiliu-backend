from apps.queue.urls import queue_api_url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    queue_api_url
)