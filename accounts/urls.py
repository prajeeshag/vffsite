from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('<str:for_view>/', views.signup_passwdreset, name='signup_passwdreset'),
    path('profile/', views.home, name='home'),
]
