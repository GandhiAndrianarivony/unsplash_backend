import json
import jwt
from datetime import datetime as dt_datetime, timezone

from django.conf import settings

from apps.users.models import User


def authenticate_header(token):
    """Check if user has requested authentication token and check it if not yet expired."""
    try:
        # Decode the JWT token
        decoded_token = jwt.decode(
            token.split()[1], settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        decoded_token = json.loads(decoded_token["payload"])

        expiration_time = dt_datetime.fromisoformat(decoded_token["exp"]).astimezone(
            timezone.utc
        )
        now = dt_datetime.now(timezone.utc)

        if expiration_time < now:
            raise jwt.ExpiredSignatureError("Token has expired")

        # Extract user information from the token payload
        username = decoded_token.get(
            "username", None
        )  # Assuming username is stored in the token payload

        # Retrieve the user based on the username
        user = User.objects.get(username=username)

        return user

    except jwt.ExpiredSignatureError as e:
        return str(e)
