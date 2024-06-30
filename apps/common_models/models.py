from django.db import models

from .utils import upload_to


# Create your models here.
class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseImage(TimeStamped):
    file_name = models.CharField(max_length=255, null=True)
    image_url = models.ImageField(upload_to=upload_to, null=True)
    base_url = models.TextField(null=True)

    class Meta:
        abstract = True
