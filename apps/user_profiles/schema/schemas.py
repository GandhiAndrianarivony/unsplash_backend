import uuid

import strawberry
from strawberry.types import Info
from strawberry.file_uploads import Upload


from rest_framework import status

from infinix import helpers

from apps.authentications.authentications import IsAuthenticated
from apps.user_profiles.models import UserProfile
from infinix.common_schema.types import JSON


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
            current_user_profile = user.profile
            u_profile = UserProfile.objects.get(user=user)
            u_profile.delete()
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
