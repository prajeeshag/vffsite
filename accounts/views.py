from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm

@login_required
def home(request):
    return render(request, 'registration/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('accounts:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form':form})
    # return HttpResponse('Signup page U/C')

