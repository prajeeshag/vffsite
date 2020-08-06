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
from mySmartFields.fields import AvatarPreview
from mySmartFields.widgets import DatePickerInput


class profileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        if hasattr(self.user, 'profile'):
            profile = self.user.profile
        else:
            profile = None

        super().__init__(*args, **kwargs, instance=profile)

        self.fields['address'].widget.attrs['rows'] = 5
        self.fields['date_of_birth'].widget = DatePickerInput(
            startOffset=100, endOffset=10)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            AvatarPreview('profile_picture'),
            RowCol('first_name', 'last_name'),
            RowCol('date_of_birth', 'email'),
            RowCol('address', RowCol('pincode', 'post_office', col_css='col-12')),
            RowCol('district', 'state'),
            RowCol('role', 'jersey_size'),
            Submit('Submit', 'submit')
        )

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user = self.user
        if commit:
            profile.save()
        return profile


def RowCol(field1, field2, col_css='col-lg-6'):
    return(Row(Column(field1, css_class=col_css),
               Column(field2, css_class=col_css)))
