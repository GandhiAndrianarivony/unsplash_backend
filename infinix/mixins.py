from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from apps.images import services
from apps.authentications.services import authenticate_header


class ImageMixin:
    """Used for REST"""
    @action(
        methods=["post"],
        detail=False,
        url_path="upload",
    )
    def upload_image(self, request, *args, **kwargs):
        """Used to save uploaded images"""

        # Get image from request
        image = request.FILES.get("image")
        user = authenticate_header(request.headers["Authorization"])

        services.save_image(image, user)

        return Response(status=status.HTTP_201_CREATED)
