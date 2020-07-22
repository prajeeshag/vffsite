from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Button, Field

from .models import User

class signupForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('mobile_number',)

    def __init__(self, *args, tabActive=True, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        formStart=HTML('<form method="post"> {% csrf_token %}')
        formEnd=HTML('</form>')
        self.active="active"
        flds=self.fields
        if not tabActive:
            self.active=""
        self.helper.layout = Layout( Div(
            formStart,
            Field('mobile_number', placeholder=flds['mobile_number'].label),
            Field('password1',placeholder=flds['password1'].label),
            Field('password2',placeholder=flds['password2'].label), 
            Submit('signup', 'Sign Up', css_class="btn-danger btn-block"),
            formEnd,
            Button('frgtpswd','Forgot password?',css_class="btn-link btn-block"),
            css_class="tab-pane frost p-3 "+self.active, id="signup"),)


class loginForm(AuthenticationForm):

    def __init__(self, *args, tabActive=True, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        formStart=HTML('<form method="post"> {% csrf_token %}')
        formEnd=HTML('</form>')

        self.active="active"
        if not tabActive:
            self.active=""

        flds=self.fields
        self.helper.layout = Layout( Div( 
            formStart, 
            Field('username',placeholder=flds['username'].label),
            Field('password',placeholder=flds['password'].label),
            Submit('login', 'Login', css_class="btn-success btn-block"),
            formEnd,
            Button('frgtpswd','Forgot password?',css_class="btn-link btn-block"),
            css_class="tab-pane frost p-3 "+self.active, id="login"),)
