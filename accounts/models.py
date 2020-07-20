from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex='^(\d{10})$', message='Phone number must be ten digits')
    mobile_number = models.CharField(_('Mobile_number'),validators=[phone_regex], max_length=10, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    address_1 = models.CharField(_('Address line 1'), max_length=250, blank=True)
    address_2 = models.CharField(_('Address line 2'), max_length=250, blank=True)
    post_office = models.CharField(_('Post Office'), max_length=50, blank=True)
    district = models.CharField(_('District/City'), max_length=50, blank=True)
    state = models.CharField(_('State'), max_length=50, blank=True)
    country = models.CharField(_('Country'), max_length=50, blank=True)
    email = models.EmailField(_('Email address'), max_length=50, blank=True, null=True, unique=True)
    email_validated = models.BooleanField(default=True,editable=False)
    JERSERY_SIZE_CHOICES = [
            ('XS', 'Extra small'),
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra large'),
            ('2XL', 'Double extra large'),
            ('3XL', 'Triple extra large')]
    jersey_size = models.CharField(_('Jersey Size'), max_length=3,
        choices=JERSERY_SIZE_CHOICES, default='M', blank=True)
    
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

