"""Deepfake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import  views
urlpatterns = [
    path('',views.Register_Data),
    path('/email_validation/<str:cipher_text>',views.Validate_email_Link),
    path('/resend_verification_link',views.resend_email_verify),
    path('/reset_password_',views.reset_password_link_gen),
    path('/reset_password_/<str:cipher_text>',views.reset_password)
]
