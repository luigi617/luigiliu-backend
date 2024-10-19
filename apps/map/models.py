from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import TimeStampedModel
from apps.user.models import User

import os



def company_image(instance, filename):
    folder_name = f'map/company_image/'
    return os.path.join(folder_name, filename)

class Marker(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    company_image = models.ImageField(upload_to=company_image, null=True, blank=True,)
    company_name =  models.CharField(max_length=255)
    address =  models.CharField(max_length=255)
    phone_number = PhoneNumberField(blank=True, null=True)
    tags =  models.TextField(blank=True)
    opening_hours =  models.TextField()
    created_by = models.ForeignKey(User, related_name="markers", on_delete=models.PROTECT)
