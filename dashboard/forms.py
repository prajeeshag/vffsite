from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Submit, Row, Column, Div, HTML, Button, Field)
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FieldWithButtons, StrictButton)
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import (authenticate, password_validation)
from django.core.exceptions import SuspiciousOperation


from accounts.models import User, Profile


class profileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
