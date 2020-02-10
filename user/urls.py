from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login/v1/', views.user_login),
    url(r'register/v1/', views.user_registration),
    ]