"""Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views


urlpatterns = [
    path('', views.authorization, name='authorization'),
    path('recruitRegistration', views.recruitRegistration, name='recruitRegistration'),
    # path('recruit/<int:pk>/test', views.recruitTest, name='recruitTest'),
    path('recruit/test', views.recruitTest, name='recruitTest'),
    path('sithRegistration', views.sithRegistration, name='sithRegistration'),
    path('almostSuccessfulRecruits', views.almostSuccessfulRecruits, name='almostSuccessfulRecruits'),
    path('recruitResults/<int:pk>', views.recruitResults, name='recruitResults'),

    path('sithHandShadow', views.sithHandShadow, name='sithHandShadow'),
    path('sithHandShadowMore1', views.sithHandShadowMore1, name='sithHandShadowMore1'),

]
