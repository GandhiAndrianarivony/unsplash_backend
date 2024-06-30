import typing

from rest_framework import status
from django.db.models import Q

import strawberry
from strawberry.types import Info
from strawberry.file_uploads import Upload
import strawberry_django
from strawberry_django.type import UNSET

from apps.images.models import (
    Image,
    ImageCollection,
    Collection,
)
from apps.images.filters import ImageFilter, CollectionFilter
from apps.images import exceptions, tasks, helpers as image_helpers, services
from apps.authentications.authentications import IsAuthenticated
from apps.users.services import create_default_profile

from infinix.common_schema.types import JSON
from infinix import helpers

from .types import ImageTypeNode, CollectionTypeNode, TCollectionResponse, HTTPResponse


@strawberry.type
class Query:
    node: strawberry.relay.Node = strawberry.relay.node()

    @strawberry.relay.connection(
        strawberry.relay.ListConnection[ImageTypeNode],
        description="""Get list of images""",
    )
    def get_images(
        self,
        info: Info,
        filters: typing.Optional[ImageFilter] = UNSET,
    ) -> typing.List[ImageTypeNode]:
        qs = Image.objects.all()

        if filters:
            qs = strawberry_django.filters.apply(filters, qs)

        return qs

    @strawberry.relay.connection(
        strawberry.relay.ListConnection[ImageTypeNode], description="""Search images"""
    )
    def searches(self, search: str = None) -> typing.List[ImageTypeNode]:
        qs = Image.objects.all()
        if search:
            qs = qs.filter(
                Q(category__icontains=search)
                | Q(description__icontains=search)
                | Q(ai_description__icontains=search)
            )
        return qs

    @strawberry.relay.connection(
        strawberry.relay.ListConnection[CollectionTypeNode],
        description="Get user's collections",
        permission_classes=[IsAuthenticated],
    )
    def get_collections(
        self,
        info: Info,
        filters: typing.Optional[CollectionFilter] = UNSET,
    ) -> typing.List[CollectionTypeNode]:
        user = info.context.request.user
        user_collections = user.collections.all()

        if filters:
            user_collections = strawberry_django.filters.apply(
                filters, user_collections
            )
        return user_collections

    @strawberry.relay.connection(
        strawberry.relay.ListConnection[ImageTypeNode],
        description="Get images within a given collection",
        permission_classes=[IsAuthenticated],
    )
    def get_images_in_collection(
        self, info: Info, collection_id: str
    ) -> typing.List[ImageTypeNode]:
        res = []
        user = info.context.request.user

        try:
            collection_id = helpers.get_id(collection_id)
            collection = Collection.objects.filter(
                Q(user=user) & Q(id=collection_id)
            ).first()
        except Collection.DoesNotExist:
            raise exceptions.CollectionNotFound(
                code=status.HTTP_400_BAD_REQUEST,
                detail="Collection does not exist",
                info=info,
            )
        im_collections = collection.images.all().prefetch_related("image")

        return [ic.image for ic in im_collections]


# SW1hZ2VUeXBlTm9kZTox [image_id]; Q29sbGVjdGlvblR5cGVOb2RlOjE= [collection_id]


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def upload_file(self, info: Info, file: Upload) -> JSON:
        """Upload image file"""

        user = info.context.request.user

        try:
            _ = user.profile
        except:
            create_default_profile(user)

        try:
            fn = image_helpers.save_uploaded_file(file, dest="temp")
        except:
            helpers.set_status_code(info=info, status_code=status.HTTP_400_BAD_REQUEST)
            return {"ErrorMessage": "Wrong upload! Check your file"}
        tasks.save_image.delay(filename=fn, user_id=user.id)

        return {"status": "[INFO] File uploaded"}

    @strawberry.mutation(
        permission_classes=[IsAuthenticated], description="Delete image"
    )
    def delete_image(self, info: Info, image_id: str) -> JSON:
        """Delete image on database and its corresponding file"""

        try:
            img_id = helpers.get_id(image_id)
            image = Image.objects.get(
                id=img_id, user=info.context.request.user
            )  # Owned image can only be deleted
            services.delete_image(image, info)
        except Image.DoesNotExist:
            raise exceptions.ImageNotFound(
                code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image of id: {image_id} not found",
                info=info,
            )
        return {"message": f"Image of id: {image_id} deleted"}

    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
        description="""
        Add image description.
        The description should describe the content of the image.
        Example: Dog run on the grass
        """,
    )
    def add_description(
        self, info: Info, description: str, image_id: str
    ) -> ImageTypeNode:
        """Add Description manually"""

        try:
            img_id = helpers.get_id(image_id)
            image = Image.objects.get(id=img_id)
            image.description = description
            image.save()
        except Image.DoesNotExist:
            raise exceptions.ImageNotFound(
                code=status.HTTP_400_BAD_REQUEST,
                detail="Image not found",
                info=info,
            )

        return image

    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
        description="Create a new collection",
    )
    def create_collection(self, info, name: str) -> TCollectionResponse:
        """Create a new collection"""

        user = info.context.request.user

        # TODO: check if collection name already exists in user's collections
        name = name.lower()
        # collection_names = Collection.objects.values_list("name", flat=True)
        _ = Collection.objects.filter(name=name, user=user).first()
        if _:
            return TCollectionResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message="FAILED",
                error_message=f"⚠️ Named Collection {name.capitalize()} already exists",
            )
        else:
            Collection.objects.create(name=name, user=user)
            return TCollectionResponse(
                status_code=status.HTTP_201_CREATED,
                status_message="COMPLETED",
            )

        # if name in collection_names:
        #     helpers.set_status_code(info, status.HTTP_208_ALREADY_REPORTED)
        #     return {"message": f"Collection with name {name} already exists"}

        # helpers.set_status_code(info, status.HTTP_201_CREATED)
        # return {"message": f"New collection ({name}) created."}

    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
        description="""Add image to a collection""",
    )
    def add_to_collection(
        self,
        info,
        image_id: str,
        collection_id: str,
    ) -> ImageTypeNode:
        """Add a new image to the collection"""

        try:
            # Get image
            img_id = helpers.get_id(image_id)
            image = Image.objects.get(id=img_id)
        except Image.DoesNotExist:
            raise exceptions.ImageNotFound(
                code=status.HTTP_400_BAD_REQUEST,
                detail="Image not found",
                info=info,
            )

        try:
            # Get Collection
            collection_id = helpers.get_id(collection_id)
            collection = Collection.objects.get(id=collection_id)
        except Collection.DoesNotExist:
            raise exceptions.CollectionNotFound(
                code=status.HTTP_400_BAD_REQUEST,
                detail="Collection not found",
                info=info,
            )

        # TODO: Check if the image exists in the collection
        img_collection = ImageCollection.objects.filter(
            Q(collection=collection) & Q(image=image)
        ).first()

        if not img_collection:
            img_collection = ImageCollection.objects.create(
                collection=collection, image=image
            )

        return image

    @strawberry_django.mutation(
        description="Remove an image from a collection",
        permission_classes=[IsAuthenticated],
    )
    def remove_image_from_collection(
        self, info: Info, image_id: str, collection_id: str
    ) -> HTTPResponse:
        try:
            image_id = helpers.get_id(image_id)
            collection_id = helpers.get_id(collection_id)

            image_collections = ImageCollection.objects.filter(
                Q(image__id=image_id) & Q(collection__id=collection_id)
            )
        except ImageCollection.DoesNotExist:
            return HTTPResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message="FAILED",
            )

        image_collections.delete()

        return HTTPResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            status_message="Unable to remove image.",
        )

    @strawberry_django.mutation(
        description="Like image",
        permission_classes=[IsAuthenticated],
    )
    def like_image(self, info: Info, image_id: str) -> HTTPResponse:
        user = info.context.request.user
        try:
            image_id = helpers.get_id(image_id)
            image = Image.objects.filter(id=image_id).first()

            # Like the image
            user.likes.add(image)
        except Image.DoesNotExist:
            return HTTPResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message=f"Image with id {image_id} not found",
            )
        return HTTPResponse(
            status_code=status.HTTP_200_OK, status_message="Successfully liked image"
        )
    
    @strawberry_django.mutation(
        description="Unlike image",
        permission_classes=[IsAuthenticated]
    )
    def unlike_image(self, info: Info, image_id: str) -> HTTPResponse:
        user = info.context.request.user

        try:
            image_id = helpers.get_id(image_id)
            image = Image.objects.filter(id=image_id).first()
            user.likes.remove(image)
        except Image.DoesNotExist:
            return HTTPResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message=f"Image with id {image_id} not found",
            )
        return HTTPResponse(
            status_code=status.HTTP_200_OK, status_message="Successfully unliked image"
        )
    