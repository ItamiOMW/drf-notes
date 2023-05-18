from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager
from .validators import validate_password

class User(AbstractUser, PermissionsMixin):

    username = None
    email = models.EmailField(unique=True)

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    password = models.CharField(validators=[validate_password, ])
    password_reset_code = models.CharField(max_length=6, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
