import pathlib

from django.db import models

from apps.users.models import User
from apps.common_models.models import TimeStamped


def upload_to(instance, filename):
    fn = instance.file_name
    ext = pathlib.Path(filename).suffix
    return f"{fn}{ext}"


class Image(models.Model):
    user = models.ForeignKey(
        User, related_name="images", on_delete=models.CASCADE, null=True
    )
    users_like = models.ManyToManyField(User, related_name="likes")
    file_name = models.CharField(max_length=255, null=True)
    image_url = models.ImageField(upload_to=upload_to, null=True)
    base_url = models.TextField(null=True)
    blurhash_code = models.TextField(null=True)
    description = models.TextField(null=True)
    ai_description = models.TextField(null=True)
    category = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.file_name}"


class Collection(TimeStamped):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(
        User,
        related_name="collections",
        on_delete=models.CASCADE,
    )


class ImageCollection(TimeStamped):
    collection = models.ForeignKey(
        Collection,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        Image,
        related_name="image_collections",
        on_delete=models.SET_NULL,
        null=True,
    )
