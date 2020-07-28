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
    phone_number = forms.CharField(
        validators=[phone_regex], label='Phone number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # heading = HTML('<h4 class="text-primary mb-4"> VFF Sign up </h4>')
        # asksignin = Div(HTML(
        # '<p> Already have an account? <a class="text-blue" href="/signin/">Sign in</a> </p>'))
        self.error_message = {
            'registered_already': _('This phone number is already registered! Sign in instead.')}

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'
        flds = self.fields
        self.helper.layout = Layout(
            PrependedAppendedAny('phone_number', icon1, None,
                                 placeholder=flds['phone_number'].label),
            Submit('sendOTP', 'Send OTP', css_class="btn-primary mb-3"))

    def clean_phone_number(self):
        phoneNumber = self.cleaned_data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phoneNumber)
            if user.has_usable_password():
                self.add_error(
                    'phone_number', forms.ValidationError(
                        self.error_message['registered_already'], code='registered_already'))
        except User.DoesNotExist:
            pass
        return phoneNumber

    def save(self, commit=True):
        phoneNumber = self.cleaned_data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phoneNumber)
            if not commit:
                user.delete()
        except User.DoesNotExist:
            user = User(phone_number=phoneNumber)
            user.set_unusable_password()
            if commit:
                user.save()
        return user


class SignupForm2(forms.Form):

    otp_regex = RegexValidator(
        regex='^(\d{10})$', message=_('OTP must be six digits'))
    otp = forms.CharField(validators=[otp_regex], label='OTP')

    pkey = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = {
            'invalidOTP': _('Entered OTP is invalid!')}

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-key"> </span>'
        flds = self.fields
        flds['pkey'].initial = user_id
        self.helper.layout = Layout(
            'pkey',
            PrependedAppendedAny('otp', icon1, None,
                                 placeholder=flds['otp'].label),
            Submit('verify', 'Verify', css_class="btn-primary mb-3"))
