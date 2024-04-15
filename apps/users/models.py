from django.contrib.auth import models as auth_models, hashers
from django.db import models as db_models
from django.utils.translation import gettext_lazy as _

from .choices import GenderType


class UserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, gender, **extra_fields):
        """Create non-admin user

        Return:
            - user (User): Instance of User
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self.perform_create(username, password, gender, **extra_fields)
        return user

    def create_superuser(self, username, password, gender, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.perform_create(username, password, gender, **extra_fields)

        return user

    def perform_create(self, username, password, gender, **extra_fields):
        """Create and save user"""
        if not username:
            raise ValueError("You must provide an email address")

        # email = self.normalize_email(email)
        user = self.model(
            username=username, password=password, gender=gender, **extra_fields
        )
        user.password = hashers.make_password(password)
        user.save()

        return user


class User(auth_models.AbstractUser):
    """Custom user model

    Attrs:
        - email:
        - username:
        - gender:
        - location:
        - website:
        - bio
        - interests

    """

    # username = db_models.CharField(max_length=255)
    email = db_models.EmailField(unique=True)

    gender = db_models.CharField(max_length=10, choices=GenderType.choices())
    location = db_models.TextField(null=True, blank=True)
    website = db_models.URLField(null=True, blank=True)
    bio = db_models.TextField(null=True, blank=True)
    interests = db_models.TextField(null=True, blank=True)
    phone_number = db_models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["gender", "email"]

    def __str__(self):
        return f"{self.username}"
