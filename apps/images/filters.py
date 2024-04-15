import typing

import strawberry
import strawberry_django
from strawberry_django.type import UNSET

from . import models


T = typing.TypeVar("T")


@strawberry.input
class Lookup(typing.Generic[T]):
    i_contains: typing.Optional[T] = UNSET


@strawberry_django.filters.filter(model=models.Image, lookups=True)
class ImageFilter:
    description: Lookup[str]
    ai_description: Lookup[str]
    category: Lookup[str]


@strawberry_django.filters.filter(model=models.Collection, lookups=True)
class CollectionFilter:
    name: Lookup[str]
