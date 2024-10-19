from rest_framework import serializers
from apps.article.models import Article, ArticleCategory


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ["id", "name"]

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "url_name", "user", "title", "date_added", "cover_img"]
class ArticleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "url_name", "user", "title", "content", "date_modified", "cover_img", "pdf", "category"]
    
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["user", "category", "url_name", "title", "content", "cover_img", "pdf"]
class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["user", "url_name", "title", "content", "cover_img"]


