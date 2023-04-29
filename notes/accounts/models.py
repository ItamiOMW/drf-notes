from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from accounts.manager import UserManager


class User(AbstractUser, PermissionsMixin):
    username = None

    email = models.EmailField(unique=True)
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    password_reset_verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_password_reset_verified = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
