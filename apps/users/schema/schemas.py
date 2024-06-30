import typing

from django.db import transaction

from rest_framework import status
from rest_framework.exceptions import ValidationError

import strawberry
import strawberry_django
from strawberry import asdict
from strawberry.types import Info
from strawberry_django.type import UNSET

from .types import (
    UserInput,
    UserTypeNode,
    BaseUserType,
    UserUpdatableInput,
)
from infinix.helpers import set_status_code

from apps.users.models import User
from apps.users.filters import UserFilter
from apps.users.serializers import UserSerializer
from apps.authentications.authentications import IsAuthenticated
from apps.users.services import create_default_profile


@strawberry.type
class Query:
    node: strawberry.relay.Node = strawberry.relay.node()

    @strawberry.relay.connection(
        strawberry.relay.ListConnection[UserTypeNode],
        description="Retrieve Users",
    )
    def users(
        self,
        info,
        filters: typing.Optional[UserFilter] = UNSET,
    ) -> typing.List[UserTypeNode]:

        qs = User.objects.all()
        if filters:
            qs = strawberry_django.filters.apply(filters, qs)

        return qs

    @strawberry_django.field(permission_classes=[IsAuthenticated])
    def get_current_user(self, info: Info) -> BaseUserType:
        return info.context.request.user


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, info: Info, input: UserInput) -> UserTypeNode:
        data = input.to_dict()
        data["gender"] = data["gender"].value

        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            set_status_code(info, status.HTTP_400_BAD_REQUEST)
            raise ValidationError(serializer.errors)

        with transaction.atomic():
            user = User.objects.create_user(**serializer.data)

            # TODO: Create default user profile
            create_default_profile(user)
            return user

    @strawberry_django.mutation(
        permission_classes=[IsAuthenticated],
        description="Updata user information",
    )
    def update_user_info(
        self,
        info: Info,
        input: UserUpdatableInput,
    ) -> UserTypeNode:
        """Update user information"""
        user = info.context.request.user

        data = asdict(input)
        data["gender"] = data.get("gender", None).value

        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return user
