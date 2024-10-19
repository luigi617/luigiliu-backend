from django.urls import path
from . import views
home_urlpatterns = [
    path('display-articles/', views.DispalyArticleListAPIView.as_view(), name='random_article_list'),
    path('nonogram-solver/', views.nonogram_solver_API_view, name='nonogram_solver'),
]