"""Image view"""

from rest_framework import viewsets

from infinix import mixins
from .serializers import ImageSerializer
from .models import Image


class ImageViewset(mixins.ImageMixin, viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
