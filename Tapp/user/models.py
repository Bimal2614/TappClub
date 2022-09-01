import uuid
from django.db import models
from .utils import generate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        referralCode = generate()
        email = self.normalize_email(email).lower()
        user = self.model(email=email,referralCode = referralCode, **other_fields)
        user.set_password(password)
        user.save()
        return user



class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    # user_name = models.CharField(max_length=150, unique=True)
    # first_name = models.CharField(max_length=150)
    # start_date = models.DateTimeField(default=timezone.now)
    # about = models.TextField(_(
        # 'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    referralCode = models.CharField(max_length=8, unique=True)
    # user_name = models.CharField(max_length=10, unique=True)
    # phone_num = models.CharField(max_length=15, unique=True)
    objects = CustomAccountManager()
    total_earned = models.IntegerField(default=0)
    # address = models.CharField(max_length=500, blank=True)
    # country = models.CharField(max_length=50, blank=True)
    is_subscribed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    # referred_by = models.CharField(max_length=10, blank = True, null=True)
    # Profile_image = models.ImageField(default='default.jpg', upload_to='profilePic')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email