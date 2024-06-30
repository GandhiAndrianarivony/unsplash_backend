import os
import uuid

from rest_framework import status
from django.conf import settings

import strawberry
import strawberry_django
from strawberry.types import Info
from strawberry.file_uploads import Upload


from infinix import helpers
from infinix.common_schema.types import JSON

from apps.common_models.graphql.types import BaseHttpResponse
from apps.authentications.authentications import IsAuthenticated
from apps.user_profiles.models import UserProfile, UserCoverPhoto


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def upload_user_profile_image(self, info: Info, file: Upload) -> JSON:
        """Used to upload user's profile image

        Args:
            info (Info): context
            file (Upload): file uploaded
        """
        # Get user from context
        user = info.context.request.user

        try:
            # Get user profile
            current_user_profile = user.profile  # Due to o2o
            current_user_profile.delete()
        except:
            pass

        try:
            user_profile = UserProfile.objects.create(
                user=user,
                file_name=str(uuid.uuid4()),
                image_url=file,
            )
            user_profile.base_url = str(user_profile.image_url.url)
            user_profile.save()

        except:
            helpers.set_status_code(info=info, status_code=status.HTTP_400_BAD_REQUEST)
            return {"errorMessage": "Wrong upload! Check your file"}

        return {"status": "Image Uploaded"}

    @strawberry_django.mutation(
        permission_classes=[IsAuthenticated],
        description="Change user cover image",
    )
    def change_user_cover_image(self, info: Info, file: Upload) -> BaseHttpResponse:
        """
        Function being used to change user cover image

        Args:
            file (Upload): Uploaded file

        Returns:
            BaseHttpResponse: Basic HTTP response
        """

        user = info.context.request.user

        # Check actual user cover image
        try:
            current_user_cover_image = user.cover_photo
            # Delete cover image from database
            current_user_cover_image.delete()
            # delete cover image file
            pth = settings.MEDIA_ROOT / os.path.basename(current_user_cover_image.base_url)
            os.remove(pth)
        except:
            pass

        # Create user cover image
        try:
            new_user_cover_image = UserCoverPhoto.objects.create(
                user=user,
                file_name=str(uuid.uuid4()),
                image_url=file,
            )
            new_user_cover_image.base_url = str(new_user_cover_image.image_url.url)
            new_user_cover_image.save()
        except:
            return BaseHttpResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                status_message="Unable to create new user cover image",
            )

        return BaseHttpResponse(
            status_code=status.HTTP_201_CREATED,
            status_message=f"Successfully created new user cover image for {user.username}",
        )
