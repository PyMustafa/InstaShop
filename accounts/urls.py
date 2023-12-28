from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]