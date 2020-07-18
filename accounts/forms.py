from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Button

from .models import User

class signupForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email','first_name','last_name')
        widgets = {
                'email': forms.EmailInput(attrs={'placeholder':'Email address'}),
                'first_name':forms.TextInput(attrs={'placeholder':'First name'}),
                'last_name':forms.TextInput(attrs={'placeholder':'Last name'}),
                }

    def __init__(self, *args, tabActive=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Password confirmation'})

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_show_labels = True
        formStart=HTML('<form method="post"> {% csrf_token %}')
        formEnd=HTML('</form>')
        self.active="active"
        if not tabActive:
            self.active=""
        self.helper.layout = Layout( Div(
            formStart,
            'email',
            Row(Div('first_name',css_class="col-md-6"), Div('last_name',css_class="col-md-6")), 
            'password1', 
            'password2', 
            Submit('signup', 'Sign Up', css_class="btn-danger btn-block"),
            formEnd,
            Button('frgtpswd','Forgot password?',css_class="btn-link btn-block"),
            css_class="tab-pane frost p-3 "+self.active, id="signup"),)

class loginForm(AuthenticationForm):

    def __init__(self, *args, tabActive=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder':'Password'})
        self.fields['username'].widget.attrs.update({'placeholder':'Email address'})

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        formStart=HTML('<form method="post"> {% csrf_token %}')
        formEnd=HTML('</form>')
        self.active="active"
        if not tabActive:
            self.active=""
        self.helper.layout = Layout( Div( 
            formStart, 
            'username',
            'password',
            Submit('login', 'Login', css_class="btn-success btn-block"),
            formEnd,
            Button('frgtpswd','Forgot password?',css_class="btn-link btn-block"),
            css_class="tab-pane frost p-3 "+self.active, id="login"),)
