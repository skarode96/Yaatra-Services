from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'daily-commutes/v1/', views.view_daily_commute_list),
    url(r'daily-commuters/v1/', views.view_daily_commute_user_list),
    url(r'daily-commute/v1/', views.create_daily_commute),
    url(r'daily-commute/v1/', views.delete_daily_commute),
    ]