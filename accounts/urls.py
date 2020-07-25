from django.contrib import admin
from django.urls import path, include
from . import views

app_name='accounts'

urlpatterns = [
    path('signin/', views.signin, name='signin'), 
    path('signup/', views.signup, name='signup'), 
    path('profile/', views.home, name='home'),
]
