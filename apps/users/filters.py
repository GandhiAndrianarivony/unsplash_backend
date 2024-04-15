import typing

import strawberry
import strawberry_django
from strawberry_django.type import UNSET

from . import models


T = typing.TypeVar("T")


@strawberry.input
class UserLookup(typing.Generic[T]):
    i_contains: typing.Optional[T] = UNSET


@strawberry_django.filters.filter(models.User, lookups=True)
class UserFilter:
    email: UserLookup[str]
