from django.contrib.auth.models import AbstractUser, User
from django.db import models


def user_dir_path(instance, filename):
    return f"users/user_{instance.username}/{filename}"


class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to=user_dir_path, default='users/default_avatar.png')

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return f"User {self.username}"
