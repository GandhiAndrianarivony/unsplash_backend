import typing

import strawberry
import strawberry_django

from apps.images import models


@strawberry_django.type(model=models.User)
class ImageOwnerNode(strawberry.relay.Node):
    id: strawberry.relay.NodeID[int]
    username: strawberry.auto
    email: strawberry.auto
    gender: strawberry.auto
    location: strawberry.auto
    website: strawberry.auto
    bio: strawberry.auto
    interests: strawberry.auto
    phone_number: strawberry.auto


@strawberry_django.type(model=models.Image)
class ImageTypeNode(strawberry.relay.Node):
    id: strawberry.relay.NodeID[int]
    file_name: strawberry.auto
    image_url: strawberry.auto
    base_url: strawberry.auto
    blurhash_code: strawberry.auto
    description: strawberry.auto
    ai_description: strawberry.auto
    category: strawberry.auto
    created_at: strawberry.auto
    user: ImageOwnerNode


@strawberry_django.type(model=models.Collection)
class CollectionTypeNode(strawberry.relay.Node):
    id: strawberry.relay.NodeID[int]
    name: strawberry.auto
    