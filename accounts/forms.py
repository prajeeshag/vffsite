from django.contrib.auth.forms import UserCreationForm as UserCreationForm_auth

from .models import User

class UserCreationForm(UserCreationForm_auth):

    class Meta(UserCreationForm_auth):
        model = User
        fields = ('email',)
