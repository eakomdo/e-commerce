from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class BaseUser(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields)
    