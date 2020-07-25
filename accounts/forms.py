from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Button, Field
from crispy_forms.bootstrap import PrependedText
from django.utils.translation import ugettext_lazy as _

from .models import User

class signupForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('mobile_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        # self.helper.form_tag = False
        # self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        # formStart=HTML('<form method="post"> {% csrf_token %}')
        # formEnd=HTML('</form>')
        flds=self.fields
        heading=HTML('<h4 class="text-primary mb-4"> VFF Sign up </h4>')
        asksignin=Div(HTML('<p> Already have an account? \
                <a class="text-blue" href="/signin/">Sign in</a> </p>'))
        icon1='<span href="" class="mdi mdi-cellphone-iphone"> </span>'
        icon2='<a href="" class="mdi mdi-eye-off"> </a>'
        self.helper.layout = Layout( 
            heading,
            PrependedText('mobile_number',icon1,placeholder=flds['mobile_number'].label),
            PrependedText('password1',icon2,placeholder=flds['password1'].label),
            PrependedText('password2',icon2,placeholder=flds['password2'].label),
            Submit('signup', 'Sign up', css_class="btn-primary btn-block mb-4"),
            asksignin)


class signinForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        # self.helper.form_tag = False
        # self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        # formStart=HTML('<form method="post"> {% csrf_token %}')
        # formEnd=HTML('</form>')

        heading=HTML('<h4 class="text-primary mb-4"> VFF Sign in </h4>')
        asksignup=Div(HTML('<p> Already have an account? \
                <a class="text-blue" href="/signup/">Sign up</a> </p>'))
        flds=self.fields
        self.helper.layout = Layout(
            heading,
            PrependedText('username','+91',placeholder=flds['username'].label),
            Field('password',placeholder=flds['password'].label),
            Submit('signin', 'Sign in', css_class="btn-primary btn-block mb-3"),
            asksignup,
            Button('frgtpswd','Forgot password?',css_class="btn-link btn-block"))


class OTPVerificationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'invalid_otp': _("Invalid OTP"),
    }
    otp = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_("Enter the OTP recieved for verification."))

    class Meta:
        model = User
        fields = ("mobile_number",)

    def verify_otp(self):

