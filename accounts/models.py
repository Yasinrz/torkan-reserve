from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not name:
            raise ValueError("Users must have a name")
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not password:
            raise ValueError("Superuser must have a password")
        if not phone_number:
            raise ValueError("Superuser must have a phone number")

        return self.create_user(phone_number, name='Admin', password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True,verbose_name=_('phone number'))
    name = models.CharField(max_length=100,verbose_name=_('First and last name'))
    is_active = models.BooleanField(default=True , verbose_name=_('is active ?'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff ?'))
    is_superuser = models.BooleanField(default=False , verbose_name=_('is superuser ?'))
    date_joined = models.DateTimeField(default=timezone.now ,verbose_name=_('date joined'))

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"    {_('user')}  {self.name}  ,  {self.phone_number}"