from rest_framework import serializers
from apps.article.models import Article
from apps.article.serializers import ArticleCategorySerializer

class DisplayArticleListSerializer(serializers.ModelSerializer):
    category = ArticleCategorySerializer()
    class Meta:
        model = Article
        fields = ["id", "url_name", "user", "title", "date_added", "cover_img", "category"]



