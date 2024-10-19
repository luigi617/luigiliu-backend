from django.urls import path
from . import views

map_urlpatterns = [
    path('map/markers/', views.MarkerListAPIView.as_view(), name='marker_list'),
    path('map/markers/creation/', views.MarkerCreationAPIView.as_view(), name='marker_creation'),
]