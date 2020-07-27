from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import pyotp

from .forms import signupForm, signinForm, otpForm1, otpForm2

@login_required
def home(request):
    return render(request, 'registration/home.html')


def signin(request):
    if request.method == 'POST':
        if settings.DEBUG:
            print(request.POST)
        form = signinForm(None, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('accounts:home')

    else:
        form = signinForm()

    return render(request, 'registration/base.html', {'form':form,})



def signup(request):
    if request.method == 'POST':
        if settings.DEBUG:
            print(request.POST)
        if 'sendOTP' in request.POST:
            form = otpForm1(request.POST)
            if form.is_valid():
                phone_number=form.cleaned_data.get('phone_number')
                form = otpForm2()
                form.send_otp()
        elif 'verifyOTP' in request.POST:
            token = request.POST['otp'][0]
            if form.totp.verify(token):
                return redirect('accounts:home')
        elif 'submit' in request.POST:
            user=form.save()
            login(request,user)
            return redirect('accounts:home')
    else:
        form = otpForm1()

    return render(request, 'registration/base.html', {'form':form,})


