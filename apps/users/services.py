import uuid
from apps.images.services import pil_to_inmemory_uploaded_file
from PIL import Image
from apps.user_profiles.models import UserProfile


def create_default_profile(user):
    image_default_profile_path = "default_user_profile.jpg"
    image = Image.open(image_default_profile_path)
    in_memory_image = pil_to_inmemory_uploaded_file(image, image_default_profile_path)
    user_profile = UserProfile.objects.create(
        user=user,
        file_name=str(uuid.uuid4()),
        image_url=in_memory_image,
    )
    user_profile.base_url = str(user_profile.image_url.url)
    user_profile.save()
