from django.urls import path
from .import views

urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('resend_activation', views.resend_activation, name='resend_activation'),
    path('sign_in',views.sign_in,name='sign_in')
]