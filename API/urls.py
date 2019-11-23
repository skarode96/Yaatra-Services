from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login/v1/', views.login),
    url(r'dailycommute/v1/', views.daily_commute_recommender),
    url('', views.index, name='index'),
]