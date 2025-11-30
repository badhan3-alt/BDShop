
from . import views

from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgetpass/', views.forgotPassword, name='forgotpass'),

    path('forgot-password/', views.forgotPassword, name='forgotPassword'),
    path('reset-password-validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset-password/', views.resetPassword, name='resetPassword'),
    path('reset/<uidb64>/<token>/', views.resetPassword, name='resetPassword'),




]
