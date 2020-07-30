from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Submit, Row, Column, Div, HTML, Button, Field)
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FieldWithButtons, StrictButton)
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import (authenticate, password_validation)
from django.core.exceptions import SuspiciousOperation

from .fields import PrependedAppendedAny


from .models import User
from .misc import TOTPDevice


hSignup = HTML('<h4 class="text-primary mb-4"> VFF Sign up </h4>')
hSignin = HTML('<h4 class="text-primary mb-4"> VFF Sign in </h4>')
asksignin = Div(HTML(
    '<p> Already have an account? <a class="text-blue" href="/signin/">Sign in</a> </p>'))
asksignup = Div(HTML(
    '<p> Do not have an account? <a class="text-blue" href="/signup/">Sign up</a> </p>'))
forgotPwd = Div(
    HTML('<a class="text-blue" href="/passwordreset/">Forgot password?</a>'))


class SignupForm1(forms.ModelForm):

    class Meta:
        model = User
        fields = ('phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'
        flds = self.fields
        self.helper.layout = Layout(
            hSignup,
            PrependedAppendedAny('phone_number', icon1, None,
                                 placeholder=flds['phone_number'].label),
            Submit('_sendOTP', 'Send OTP', css_class="btn-primary mb-3"),
            asksignin)

    def save(self):
        user = super().save(commit=False)
        return user

    def clean(self):
        super().clean()
        phone_number = self.cleaned_data.get('phone_number')


class numberVerifyForm(forms.Form):

    regex = RegexValidator(
        regex='^(\d{10})$', message=_('Phone number must be 10 digits'))
    phone_number = forms.CharField(
        validators=[regex], label='Phone number', max_length=10)

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        header = kwargs.pop('Verify', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'
        flds = self.fields
        heading = HTML('<h4 class="text-primary mb-4"> '+header+' </h4>')
        self.helper.layout = Layout(
            heading,
            PrependedAppendedAny('phone_number', icon1, None,
                                 placeholder=flds['phone_number'].label),
            Submit('_sendOTP', 'Send OTP', css_class="btn-primary mb-3"),
            asksignin)

    def clean(self):
        super().clean()
        phoneNumber = self.cleaned_data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phoneNumber)
        except User.exceptions.DoesNotExist:
            raise forms.ValidationError(
                'An account with this number does not exist.', code='accountNotExist')
        if self.session is not None:
            self.session['phone_number'] = phoneNumber
            totpName = totpKey(phoneNumber)
            if totpName in self.session:
                del self.session[totpName]
        return phoneNumber


class OTPForm(forms.Form):

    otp_regex = RegexValidator(
        regex='^(\d{6})$', message=_('OTP must be six digits'))
    otp = forms.CharField(validators=[otp_regex], label='OTP', max_length=6)

    def __init__(self, *args, **kwargs):

        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)
        self.phone_number = self.session['phone_number']
        totpName = totpKey(self.phone_number)
        self.totpName = totpName

        if totpName in self.session:
            totpData = self.session[totpName]
            self.totp = TOTPDevice(**totpData)
        else:
            self.totp = TOTPDevice()
            self.session[totpName] = vars(self.totp)

        self.error_message = {
            'invalidOTP': _('Entered OTP is invalid!')}

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-key"> </span>'
        flds = self.fields
        flds['otp'].help_text = ' '.join(['OTP sent to', self.phone_number])
        self.helper.layout = Layout(
            PrependedAppendedAny('otp', icon1, None,
                                 placeholder=flds['otp'].label),
            Submit('_verify', 'Verify', css_class="btn-primary mb-3"),
            HTML('<i>token testing: '+self.totp.generate_token()+'</i>'))

    def clean_otp(self):
        token = self.cleaned_data.get('otp')
        if self.totp.verify_token(token):
            del self.session[self.totpName]
        else:
            raise forms.ValidationError(
                self.error_message['invalidOTP'], code='invalidOTP')
        return token


class SignupForm2(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
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

    class Meta:
        model = User
        fields = ('phone_number',)

    def __init__(self, *args, **kwargs):

        self.session = kwargs.pop('session')

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        icon1 = '<span class="input-group-text mdi mdi-key"> </span>'
        flds = self.fields

        flds['phone_number'].widget = forms.HiddenInput()
        flds['phone_number'].initial = self.session['phone_number']

        self.helper.layout = Layout(
            hSignup,
            'phone_number',
            PrependedAppendedAny('password1', icon1, None,
                                 placeholder=flds['password1'].label),
            PrependedAppendedAny('password2', icon1, None,
                                 placeholder=flds['password2'].label),
            Submit('_signup', 'Sign up', css_class="btn-primary mb-3"))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number_initial = self.fields['phone_number'].initial
        if phone_number != phone_number_initial:
            raise SuspiciousOperation('Phone number changed!!!')
        return phone_number

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
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
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

        self.helper.layout = Layout(
            hSignin,
            PrependedAppendedAny('username', icon1, None,
                                 placeholder=flds['username'].label),
            PrependedAppendedAny('password', icon2, None,
                                 placeholder=flds['password'].label),
            Submit('_signin', 'Sign in', css_class="btn-primary mb-3"),
            asksignup)


def totpKey(x):
    return "".join(['totp', x])
