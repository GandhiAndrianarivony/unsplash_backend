from rest_framework import serializers

from apps.users.serializers import UserSerializer
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Image
        fields = '__all__'