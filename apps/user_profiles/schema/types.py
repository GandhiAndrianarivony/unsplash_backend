import strawberry_django
from strawberry import auto

from apps.user_profiles.models import (
    UserProfile,
    UserCoverPhoto,
)
from apps.common_models.graphql.types import BaseImageType


@strawberry_django.type(model=UserProfile)
class UserProfileType:
    base_url: auto


@strawberry_django.type(model=UserCoverPhoto)
class UserCoverPhotoType(BaseImageType): ...
