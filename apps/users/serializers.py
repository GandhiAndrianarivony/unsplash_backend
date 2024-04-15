from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        private_fields = [
            # "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        for field in self.Meta.private_fields:
            repr.pop(field, None)

        return repr
