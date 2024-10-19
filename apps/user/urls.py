from django.urls import path
from . import views
users_urlpatterns = [
    path('users/<int:pk>/', views.UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile'),
]