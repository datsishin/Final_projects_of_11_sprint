from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from api.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    email = models.EmailField(verbose_name='email', unique=True)
    confirmation_code = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    username = models.SlugField(verbose_name='username', max_length=150, unique=True, blank=True, null=True)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.email
