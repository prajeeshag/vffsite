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

from mySmartFields.fields import PrependedAppendedAny


from .models import User
from .misc import TOTPDevice


class numberVerifyForm(forms.Form):

    error_messages = {'accExist': _('An account already exist with this Phone Number!'),
                      'accNotExist': _('Account does not exist with this Phone Number!')}

    regex = RegexValidator(
        regex='^(\d{10})$', message=_('Phone number must be 10 digits'))
    phone_number = forms.CharField(validators=[regex],
                                   label='Phone number', max_length=10)

    def __init__(self, *args, **kwargs):

        self.session = kwargs.pop('session')
        self.is_signup = kwargs.pop('is_signup', True)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'

        flds = self.fields

        for key, fld in flds.items():
            fld.widget.attrs['placeholder'] = fld.label

        self.helper.layout = Layout(
            PrependedAppendedAny('phone_number', icon1, None),
            Submit('_sendOTP', 'Send OTP', css_class="btn-primary mb-3"))

    def clean(self):
        super().clean()
        phone_number = self.cleaned_data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            if self.is_signup is True:
                raise forms.ValidationError(self.error_messages[
                    'accExist'], code='accExist')
        except User.DoesNotExist:
            if self.is_signup is False:
                raise forms.ValidationError(
                    self.error_messages['accNotExist'], 'accNotExist')

        self.session['phone_number'] = phone_number
        print(self.session)


class OTPForm(forms.Form):

    otp_regex = RegexValidator(
        regex='^(\d{6})$', message=_('OTP must be six digits'))
    otp = forms.CharField(validators=[otp_regex], label='OTP', max_length=6)

    def __init__(self, *args, **kwargs):

        self.session = kwargs.pop('session')
        super().__init__(*args, **kwargs)
        self.phone_number = self.session['phone_number']

        if 'totp' in self.session:
            totpData = self.session['totp']
            self.totp = TOTPDevice(**totpData)
        else:
            self.totp = TOTPDevice()
            self.session['totp'] = vars(self.totp)

        self.error_message = {
            'invalidOTP': _('Entered OTP is invalid!')}

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-key"> </span>'

        flds = self.fields

        for key, fld in flds.items():
            fld.widget.attrs['placeholder'] = fld.label

        flds['otp'].help_text = ' '.join(['OTP sent to', self.phone_number])
        self.helper.layout = Layout(
            PrependedAppendedAny('otp', icon1, None),
            Submit('_verify', 'Verify', css_class="btn-primary mb-3"),
            Div(HTML('<i>token testing: '+self.totp.generate_token()+'</i>')))

    def clean_otp(self):
        token = self.cleaned_data.get('otp')
        if self.totp.verify_token(token) is not True:
            raise forms.ValidationError(
                self.error_message['invalidOTP'], code='invalidOTP')
        return token


class passwdSetForm(forms.Form):
    error_messages = {'accExist': _('An account already exist with this Phone Number!'),
                      'accNotExist': _('Account does not exist with this Phone Number!'),
                      'password_mismatch': _('The two password fields didn’t match.')}

    regex = RegexValidator(
        regex='^(\d{10})$', message=_('Phone number must be 10 digits'))
    phone_number = forms.CharField(validators=[regex],
                                   label='Phone number', max_length=10)

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):

        self.session = kwargs.pop('session')
        self.is_signup = kwargs.pop('is_signup', True)

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-key"> </span>'
        flds = self.fields
        for key, fld in flds.items():
            fld.widget.attrs['placeholder'] = fld.label

        flds['phone_number'].widget = forms.HiddenInput()
        flds['phone_number'].initial = self.session['phone_number']

        self.helper.layout = Layout(
            'phone_number',
            PrependedAppendedAny('password1', icon1, None),
            PrependedAppendedAny('password2', icon1, None),
            Submit('_submit', 'Submit', css_class="btn-primary mb-3"))

    def clean(self):
        super().clean()
        phone_number = self.cleaned_data.get('phone_number')
        phone_number_initial = self.fields['phone_number'].initial
        if phone_number != phone_number_initial:
            raise SuspiciousOperation('Phone number changed!!!')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        phone_number = self.session['phone_number']

        if self.is_signup is True:
            user = User(phone_number=phone_number)
        else:
            user = User.objects.get(phone_number=phone_number)

        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class SigninForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'
        icon2 = '<span class="input-group-text mdi mdi-key"> </span>'
        flds = self.fields
        for key, fld in flds.items():
            fld.widget.attrs['placeholder'] = fld.label

        self.helper.layout = Layout(
            PrependedAppendedAny('username', icon1, None),
            PrependedAppendedAny('password', icon2, None),
            Submit('_signin', 'Sign in', css_class="btn-primary mb-3"))
