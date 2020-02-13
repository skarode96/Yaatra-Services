from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'daily/<int:journey_id>/', views.view_daily_commute_list),
    url(r'daily-commuters/', views.view_daily_commute_user_list),
    url(r'daily-commute/', views.create_daily_commute),
    url(r'daily-commute/', views.delete_daily_commute),
    ]