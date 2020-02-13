from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
    path(r'daily/<int:user_id>/', views.get_daily_commutes_for_user),
    path(r'daily/user/<int:journey_id>', views.get_user_list_for_journey),
    url(r'daily/', views.create_daily_commute),
    url(r'daily-commute/', views.delete_daily_commute),
    ]