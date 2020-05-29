"""social_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views as vbase
from django.conf.urls import include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('home/',vbase.HomePage.as_view(), name='home'),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('test/', vbase.TestPage.as_view(), name='test'),
    path('thanks/', vbase.ThanksPage.as_view(), name='thanks'),
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls',namespace='tickets')),
    path('projects/', include('projects.urls',namespace='projects')),
]