from django.db import models
from datetime import datetime

# Create your models here.
class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True