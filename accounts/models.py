from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django_otp.util import random_hex
from django_otp.oath import TOTP

import time

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex='^(\d{10})$', message=_('Phone number must be ten digits'))
    phone_number = models.CharField(_('phone number'), validators=[
                                    phone_regex], max_length=10, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(_('first name'), max_length=30)

    last_name = models.CharField(_('last name'), max_length=30)

    profile_picture = models.ImageField(
        upload_to='data/avatars/')

    date_of_birth = models.DateField(_('Date of birth'))

    address = models.TextField(_('Address'), max_length=200)

    post_office = models.CharField(_('Post Office'), max_length=50)

    district = models.CharField(_('District/City'), max_length=50)

    state = models.CharField(_('State'), max_length=50)

    # country = models.CharField(_('Country'), max_length=50, default='India')

    regex = RegexValidator(
        regex='^(\d{6})$', message=_('Pincode must be six digits'))
    pincode = models.CharField(_('Pincode'), validators=[regex], max_length=6)

    email = models.EmailField(
        _('Email address'), max_length=50, blank=True, null=True, unique=True)

    email_validated = models.BooleanField(default=True, editable=False)

    JERSERY_SIZE_CHOICES = [
        ('XS', _('Extra small')),
        ('S', _('Small')),
        ('M', _('Medium')),
        ('L', _('Large')),
        ('XL', _('Extra large')),
        ('2XL', _('Double extra large')),
        ('3XL', _('Triple extra large'))]
    jersey_size = models.CharField(_('Jersey Size'), max_length=3,
                                   choices=JERSERY_SIZE_CHOICES)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
