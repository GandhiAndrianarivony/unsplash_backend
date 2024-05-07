import strawberry_django
from strawberry import auto

from apps.user_profiles.models import UserProfile

@strawberry_django.type(model=UserProfile)
class UserProfileType:
    base_url: auto