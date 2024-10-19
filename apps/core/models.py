from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    ``created`` and ``modified`` fields.
    """
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


def get_upload_to(instance, filename):
    """
    simply delegates to the `get_upload_to` method of the instance, so that AbstractImage
    subclasses can override it.
    """
    return instance.get_upload_to(filename)

class AbstractImage(models.Model):
    
    '''Abstract Model for all the Image Class in Euroingro
    '''
    title = models.CharField(max_length=255, verbose_name=_('title'), null=True, blank=True, help_text="used for image 'alt' attribute and SEO")
    file = models.ImageField(
        verbose_name=_('file'), upload_to=get_upload_to, 
        width_field='width', height_field='height', null=True, blank=True,
    )
    
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True, db_index=True)
    uploaded_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('uploaded by user'),
        null=True, blank=True, editable=False, on_delete=models.SET_NULL
    )
    class Meta:
        abstract = True
    