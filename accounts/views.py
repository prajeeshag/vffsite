from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import numberVerifyForm, OTPForm, passwdSetForm, SigninForm
from .misc import TOTPDevice


@login_required
def home(request):
    print(request.user)
    return render(request, 'registration/base.html')


class SignoutView(LogoutView):
    pass


class SigninView(LoginView):
    form_class = SigninForm
    template_name = 'registration/signin.html'


def signup_passwdreset(request, for_view):

    if for_view == 'signup':
        is_signup = True
        template = 'registration/signup.html'
        msg = _('Account created. Please sign in.')
    elif for_view == 'passwdreset':
        is_signup = False
        template = 'registration/passwdreset.html'
        msg = _('Password changed successfully')
    else:
        raise Http404(for_view+" does not exist")

    if settings.DEBUG:
        print(request.POST)

    request.session.set_expiry(0)

    if '_sendOTP' in request.POST:
        form = numberVerifyForm(
            data=request.POST, session=request.session[for_view], is_signup=is_signup)
        if form.is_valid():
            print(request.session[for_view])
            form = OTPForm(session=request.session[for_view])
    elif '_verify' in request.POST:
        form = OTPForm(data=request.POST, session=request.session[for_view])
        if form.is_valid():
            form = passwdSetForm(
                session=request.session[for_view], is_signup=is_signup)
    elif '_submit' in request.POST:
        form = passwdSetForm(
            data=request.POST, session=request.session[for_view], is_signup=is_signup)
        if form.is_valid():
            user = form.save()
            del request.session[for_view]
            messages.success(request, msg)
            return redirect('accounts:signin')
    else:
        request.session[for_view] = {}
        form = numberVerifyForm(
            session=request.session[for_view], is_signup=is_signup)

    return render(request, template, {'form': form, })
