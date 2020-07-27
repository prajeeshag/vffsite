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


class SignupForm1(forms.ModelForm):

    heading = HTML('<h4 class="text-primary mb-4"> VFF Sign up </h4>')
    asksignin = Div(HTML('<p> Already have an account? \
            <a class="text-blue" href="/signin/">Sign in</a> </p>'))

    class Meta:
        model = User
        fields = ('phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        flds = self.fields
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'

        self.helper.layout = Layout(
            signupForm.heading,
            PrependedAppendedAny('phone_number', icon1,
                                 None, placeholder=flds['phone_number'].label),
            Submit('sendOTP', 'Send OTP', css_class="btn-primary mb-3"),
            signupForm.asksignin)


class otpForm2(forms.ModelForm):

    error_messages = {
        'invalid_otp': _("Invalid OTP"),
    }

    otpregex = RegexValidator(
        regex='^(\d{6})$', message='OTP must be 6 digits')
    otp = forms.CharField(label=_("OTP"),
                          widget=forms.TextInput,
                          validators=[otpregex],
                          max_length=6)

    heading = HTML('<h4 class="text-primary mb-4"> VFF Sign up </h4>')
    asksignin = Div(HTML('<p> Already have an account? \
            <a class="text-blue" href="/signin/">Sign in</a> </p>'))

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, otpInterval=180, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        flds = self.fields
        icon2 = '<span class="input-group-text mdi mdi-key"> </span>'

        self.helper.layout = Layout(
            signupForm.heading,
            PrependedAppendedAny('otp', icon2, None,
                                 placeholder=flds['otp'].label),
            Submit('verifyOTP', 'verify', css_class="btn-primary mb-3"),
            signupForm.asksignin)


class signupForm(UserCreationForm):

    heading = HTML('<h4 class="text-primary mb-4"> VFF Sign up </h4>')
    asksignin = Div(HTML('<p> Already have an account? \
            <a class="text-blue" href="/signin/">Sign in</a> </p>'))

    class Meta(UserCreationForm):
        model = User
        fields = ('phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        flds = self.fields
        icon1 = '<span class="input-group-text mdi mdi-cellphone-iphone"> </span>'
        self.helper.layout = Layout(
            signupForm.heading,
            PrependedAppendedAny('phone_number', icon1,
                                 None, placeholder=flds['phone_number'].label),
            Submit('getOTP', 'Get OTP', css_class="btn-success mb-3"),
            signupForm.asksignin)


class signinForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        # self.helper.form_tag = False
        # self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        # formStart=HTML('<form method="post"> {% csrf_token %}')
        # formEnd=HTML('</form>')

        heading = HTML('<h4 class="text-primary mb-4"> VFF Sign in </h4>')
        asksignup = Div(HTML('<p> Already have an account? \
                <a class="text-blue" href="/signup/">Sign up</a> </p>'))
        flds = self.fields
        self.helper.layout = Layout(
            heading,
            PrependedText('username', '+91',
                          placeholder=flds['username'].label),
            Field('password', placeholder=flds['password'].label),
            Submit('signin', 'Sign in', css_class="btn-primary btn-block mb-3"),
            asksignup,
            Button('frgtpswd', 'Forgot password?', css_class="btn-link btn-block"))
