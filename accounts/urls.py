from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forget-password/', views.forget_password, name='forget-password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset-password-validate'),
    path('reset-password/', views.reset_password, name='reset-password'),

]