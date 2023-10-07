"""
URL configuration for final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from medical_bot import urls as medical_url
from image_process import urls as image_url
from login import urls as loginurl
from login import views as loginviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot_url',include(medical_url)),
    path('register',include(loginurl)),
    path('login',loginviews.login_),
    path('image_process',include(image_url))
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns # new
urlpatterns += staticfiles_urlpatterns() # new
