from PIL import Image as pil_image
import os

from celery import shared_task

from apps.images import services as image_services
from apps.users.models import User


@shared_task
def save_image(filename, user_id):
    # Get image from temp

    image = pil_image.open(filename)

    # Get image category
    image_category = image_services.predict_image_category(image)

    # TODO: Get image description

    uploaded_file = image_services.pil_to_inmemory_uploaded_file(image, filename)
    user = User.objects.get(id=user_id)

    print("[INFO] Save image")
    image = image_services.save_image(uploaded_file, user, image_category)

    # Delete image from temp
    os.remove(filename)
