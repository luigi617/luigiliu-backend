from apps.openapi.urls import open_api_url, text_page_api_url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    # open_api_url
    text_page_api_url
)