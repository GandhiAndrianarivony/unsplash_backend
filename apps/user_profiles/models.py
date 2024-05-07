from pathlib import Path
from django.db import models

from apps.users.models import User
from apps.common_models.models import TimeStamped


def upload_to(instance, filename):
    fn = instance.file_name
    ext = Path(filename).suffix
    return f"{fn}{ext}"


# Create your models here.
class UserProfile(TimeStamped):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    file_name = models.CharField(max_length=255, null=True)
    image_url = models.ImageField(upload_to=upload_to, null=True)
    base_url = models.TextField(null=True)
