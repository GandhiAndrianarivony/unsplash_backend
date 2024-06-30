from typing import Any

from strawberry.permission import BasePermission
from strawberry.types import Info

from rest_framework import status

from .services import authenticate_header
from apps.users.models import User
from infinix.helpers import set_status_code


class IsAuthenticated(BasePermission):
    message = "User not Authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool:
        request = info.context.request

        if "Authorization" in request.headers:
            jwt_token = request.headers.get("Authorization")
            user = authenticate_header(jwt_token)

            if isinstance(user, User):
                request.user = user
                return True
            else:
                self.message = str(user)

        set_status_code(info, status.HTTP_400_BAD_REQUEST)
        return False
