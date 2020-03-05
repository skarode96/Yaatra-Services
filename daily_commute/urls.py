from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'daily/schedules/', views.get_daily_commutes_for_user),
    url(r'daily/details/', views.get_journey_details),
    url(r'daily/notification/', views.daily_commuter_notification),
    url(r'daily/', views.create_daily_commute),
    url(r'daily/', views.delete_daily_commute),
    url(r'daily/', views.update_daily_commute),
    ]