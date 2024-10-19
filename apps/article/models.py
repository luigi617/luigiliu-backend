from django.db import models

from apps.core.models import TimeStampedModel
from apps.user.models import User
import os
# Create your models here.

class ArticleCategory(models.Model):
    name = models.CharField(unique=True, null=False, blank=True, max_length=255)

def cover_location(instance, filename):
    folder_name = f'articles/cover/'
    return os.path.join(folder_name, filename)
def pdf_location(instance, filename):
    folder_name = f'articles/pdf/'
    return os.path.join(folder_name, filename)

class Article(TimeStampedModel):
    url_name = models.CharField(unique=True, null=False, blank=True, max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    pdf = models.FileField(upload_to=pdf_location, null=True, blank=True)
    user = models.ForeignKey(User, related_name="articles", on_delete=models.PROTECT)
    cover_img = models.ImageField(upload_to=cover_location, null=True, blank=True)
    category = models.ForeignKey(ArticleCategory, related_name="articles", on_delete=models.PROTECT, null=True)

