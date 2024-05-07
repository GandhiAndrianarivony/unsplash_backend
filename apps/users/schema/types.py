import typing

import strawberry
import strawberry_django
from strawberry_django.type import UNSET
from strawberry import auto

from apps.images.schema import types

from apps.users import models
from apps.users.choices import GenderType
from apps.user_profiles.schema.types import UserProfileType


@strawberry_django.type(model=models.User)
class BaseUserType:
    username: auto
    email: auto
    gender: auto
    location: auto
    website: auto
    bio: auto
    interests: auto
    phone_number: auto
    profile: UserProfileType


# Define User Type
@strawberry_django.type(model=models.User)
class UserTypeNode(strawberry.relay.Node):
    id: strawberry.relay.NodeID[int]
    username: auto
    email: auto
    gender: auto
    location: auto
    website: auto
    bio: auto
    interests: auto
    phone_number: auto
    images: typing.List[types.ImageTypeNode]


@strawberry_django.input(model=models.User)
class UserInput:
    username: auto
    email: auto
    password: auto
    gender: GenderType
    location: auto
    website: auto
    bio: auto
    interests: auto
    phone_number: auto

    def to_dict(self) -> dict:
        # Initialize an empty dictionary to store the user input
        user_dict = {}

        # Iterate over the fields in the class
        for field_name in self.__annotations__:
            # Get the value of the field using getattr
            field_value = getattr(self, field_name)

            # Add the field and its value to the dictionary
            if field_value != UNSET:
                user_dict[field_name] = field_value

        return user_dict
