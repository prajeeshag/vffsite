from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import pyotp

from .forms import SignupForm1


@login_required
def home(request):
    return render(request, 'registration/home.html')


def signin(request):
    form = SignupForm1()

    return render(request, 'registration/base.html', {'form': form, })


def signup(request):
    form = SignupForm1()

    return render(request, 'registration/base.html', {'form': form, })
