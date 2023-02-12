import uuid
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, email):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            is_active=True
        )

        user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, email):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(phone_number=phone_number, email=email)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = None
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    phone_number = PhoneNumberField(unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()


    def __str__(self) -> str:
        return str(self.phone_number)