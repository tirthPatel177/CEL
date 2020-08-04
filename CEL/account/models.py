from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

DEFAULT_TIME = datetime(2020, 6, 13, 16, 0, 0)


class AccountManager(BaseUserManager):

    def create_user(self, username, email, password=None,
                    last_ans_time=DEFAULT_TIME, points=0, is_active=True,
                    staff=False, is_superuser=False, is_activated=False):
        if not username:
            raise ValueError('Users must have a unique username.')
        if not email:
            raise ValueError('Users must have an email.')
        if not password:
            raise ValueError('Users must have a password.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            # fullname=fullname
        )

        user.set_password(password)
        user.is_active = is_active
        user.staff = staff
        user.is_superuser = is_superuser
        user.is_activated = is_activated
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, fullname=None, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
            # fullname=fullname,
            staff=True,
            is_activated=True
        )
        return user

    def create_superuser(self, username, email, fullname=None, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
            # fullname=fullname,
            staff=True,
            is_superuser=True,
            is_activated=True
        )
        return user


class Account(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=200)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = AccountManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.staff

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_winner(self):
        if(self.challenged_won.count() > 0):
            return True
        else: 
            return False