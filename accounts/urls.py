from django.contrib import admin
from django.urls import path, include
from . import views

app_name='accounts'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'), 
    path('accounts/profile/', views.home, name='home'),
]
