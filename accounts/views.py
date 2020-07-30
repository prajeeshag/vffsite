from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import pyotp

from .forms import SignupForm1, SignupForm2, SignupForm3, SigninForm
from .misc import TOTPDevice


@login_required
def home(request):
    print(request.user)
    return render(request, 'registration/base.html')


class SigninView(LoginView):
    form_class = SigninForm
    template_name = 'registration/base.html'


def signup(request):

    if settings.DEBUG:
        print(request.POST)

    if '_sendOTP' in request.POST:
        form = SignupForm1(data=request.POST, session=request.session)
        if form.is_valid():
            form = SignupForm2(session=request.session)
    elif '_verify' in request.POST:
        form = SignupForm2(data=request.POST, session=request.session)
        if form.is_valid():
            form = SignupForm3(session=request.session)
    elif '_signup' in request.POST:
        form = SignupForm3(data=request.POST, session=request.session)
        if form.is_valid():
            user = form.save()
            return render(request, 'registration/base.html')
    else:
        form = SignupForm1(session=request.session)

    request.session.set_expiry(0)

    return render(request, 'registration/base.html', {'form': form, })
