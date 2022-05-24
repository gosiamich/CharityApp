"""fundraiser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from fundraiser_app.views import LandingPage, AddDonationView, FormConfirmation
from accounts.views import LoginView, RegisterView, LogOutView, UserProfileView, UpdateUserView, ChangePasswordView, \
    Password, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPage.as_view(), name='landing_page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('add_donation/', AddDonationView.as_view(), name='add_donation'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogOutView.as_view(), name='logout'),
    path('userprofile/',UserProfileView.as_view(), name='user_profile'),
    path('updateuser/', UpdateUserView.as_view(), name='update_user'),
    path('changepassword/', ChangePasswordView.as_view(), name='change_password'),
    path('form_confirmation/', FormConfirmation.as_view(), name= 'form_confirmation'),
    path('pass/', Password.as_view(template_name='fundraiser_app/change_password.html'),name='pass'),
    path('signup/', SignUpView.as_view(), name='sign_up'),
    ]
