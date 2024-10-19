from django.contrib import admin

# Register your models here.
from apps.article.models import *

admin.site.register(Article)
admin.site.register(ArticleCategory)