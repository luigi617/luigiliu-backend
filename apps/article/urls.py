from django.urls import path
from . import views
articles_urlpatterns = [
    path('articles/', views.ArticleListAPIView.as_view(), name='article_list'),
    path('article-categories/', views.ArticleCategoryListAPIView.as_view(), name='article_category_list'),
    path('articles/get/<str:url_name>/', views.ArticleRetrieveAPIView.as_view(), name='article_retrieve'),
    path('articles/creation/', views.ArticleCreationAPIView.as_view(), name='article_creation'),
    path('articles/update/', views.ArticleUpdateAPIView.as_view(), name='article_update'),
]