from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, phone_number=None, password=None):
        if not email:
            raise ValueError('User must have an email address!')

        if not username:
            raise ValueError('User must have a username!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.email_is_verified = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False, validators=[validate_email], db_index=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    email_is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
