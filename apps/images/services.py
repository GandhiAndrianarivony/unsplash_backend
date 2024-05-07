import uuid
import os
from io import BytesIO
from PIL import Image as pil_image

from strawberry.types import Info

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.conf import settings
from rest_framework import status
import environ

from apps.users.models import User
from apps.aiml.modeling.build import PreTrainModel
from apps.aiml.modeling.image_to_text.build import ImageToTextModel
from apps.aiml.engine.inference import predict
from apps.aiml.data_builder.build import build_data
from apps.aiml.data_builder.image_to_text.build import (
    build_image_to_text_model_data_processor,
)
from infinix.helpers import set_status_code

from . import helpers
from .models import Image

env = environ.Env()


def predict_image_category(image: pil_image):
    # Get Model
    model = PreTrainModel(env("CLASSIFICATION_MODEL"))

    # Build data
    data, categories = build_data(image)
    return predict(model, data, categories)


def generate_image_description(image: pil_image):
    model = ImageToTextModel(env("IMAGE_TO_TEXT_MODEL"))

    # Build data
    processor = build_image_to_text_model_data_processor()
    pixel_values = processor["image_processor"](image, return_tensors="pt").pixel_values
    generated_ids = model(pixel_values)
    generated_text = processor["tokenizer"].batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )[0]
    description = generated_text.capitalize()
    print(f"[INFO] Image description {description}")
    return description


def pil_to_inmemory_uploaded_file(image_pil, filename):
    # Create a BytesIO object to hold the image data
    image_io = BytesIO()

    # Save the PIL image to the BytesIO object
    image_pil.save(image_io, format="JPEG")  # Change format as needed

    # Create an InMemoryUploadedFile object
    memory_file = InMemoryUploadedFile(
        file=image_io,
        field_name=None,  # You can set field name if you have one
        name=filename,  # Name of the file
        content_type="image/jpeg",  # Change content type according to your image format
        size=image_io.tell(),
        charset=None,
    )

    return memory_file


def delete_image(image: Image, info: Info):
    image.delete()
    image_path = settings.MEDIA_ROOT / os.path.basename(image.base_url)
    os.remove(image_path)
    set_status_code(info, status.HTTP_200_OK)
    return


@transaction.atomic
def save_image(
    image: InMemoryUploadedFile,
    user: User,
    image_category: str,
    image_ai_description: str,
):
    blurhash_code = helpers.generate_blurhash_code(image)
    image_fn = str(uuid.uuid4())

    new_image = Image.objects.create(
        user=user,
        file_name=image_fn,
        image_url=image,
        blurhash_code=blurhash_code,
        category=image_category,
        ai_description=image_ai_description,
    )
    new_image.base_url = str(new_image.image_url.url)
    new_image.save()
    return new_image
