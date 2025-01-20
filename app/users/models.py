from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from commons.validators import ContentTypeValidator, FileSizeValidator


class UserManager(BaseUserManager):
    def create(self, username, password, **extra_fields):
        user = self.model(
            username=username.lower(),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **extra_fields):
        return self.create(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields["is_superuser"] = True
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, db_index=True, unique=True)
    image = models.FileField(
        upload_to="users/",
        blank=True,
        null=True,
        validators=[
            FileSizeValidator(15 * 1024 * 1024),
            ContentTypeValidator(
                "image/heic",
                "image/heif",
                "image/jpeg",
                "image/png",
            ),
        ],
    )
    description = models.TextField(blank=True, default="")
    last_login = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.username)
