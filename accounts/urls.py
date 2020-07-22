from django.contrib import admin
from django.urls import path, include
from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.login, name='login'), 
    path('profile/', views.home, name='home'),
]
