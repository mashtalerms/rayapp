from django.contrib.auth.base_user import AbstractBaseUser
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db import transaction


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    username = models.CharField(max_length=150, unique=True, verbose_name='Логин', default="")
    email = models.EmailField(verbose_name='Email', unique=True, default="")
    password = models.CharField(max_length=128, blank=True, default="", verbose_name='пароль')
    name = models.CharField(max_length=150, blank=True, default=None, null=True, verbose_name='Имя')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name if self.name else "USER_" + str(self.pk)
