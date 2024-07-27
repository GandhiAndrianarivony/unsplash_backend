"""
Ref: https://earthly.dev/blog/django-signals/
"""

import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image

from apps.user_profiles.models import UserCoverPhoto
from .services import pil_to_inmemory_uploaded_file

from .models import User


@receiver(post_save, sender=User)
def create_cover_photo(sender, instance, created, **kwargs):
    if created:
        image_path = "default_cover_photo.jpg"
        image = Image.open(image_path)
        image = pil_to_inmemory_uploaded_file(image, image_path)

        cover_photo = UserCoverPhoto.objects.create(
            user=instance,
            file_name=str(uuid.uuid4()),
            image_url=image,
        )
        cover_photo.base_url = str(cover_photo.image_url.url)
        cover_photo.save()

# TODO: Delete all image without owner