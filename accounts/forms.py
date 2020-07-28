from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Submit, Row, Column, Div, HTML, Button, Field)
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FieldWithButtons, StrictButton)
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from .fields import PrependedAppendedAny


from .models import User, TOTPDevice


class SignupForm1(forms.Form):

    phone_regex = RegexValidator(
        regex='^(\d{10})$', message=_('Phone number must be ten digits'))
    phone_number = forms.RegexField(
        phone_regex, max_length=10, min_length=10, label='Phone number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # heading = HTML('<h4 class="text-primary mb-4"> VFF Sign up </h4>')
        # asksignin = Div(HTML(
        # '<p> Already have an account? <a class="text-blue" href="/signin/">Sign in</a> </p>'))

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'
        flds = self.fields
        self.helper.layout = Layout(
            PrependedAppendedAny('phone_number', icon1,
                                 None, placeholder=flds['phone_number'].label),
            Submit('sendOTP', 'Send OTP', css_class="btn-primary mb-3"))
