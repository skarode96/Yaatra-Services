from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'userLogin/v1/', views.user_login),
    url(r'userRegister/v1/', views.user_registration),
    url(r'viewDailyCommutes/v1/', views.view_daily_commute_list),
    url(r'viewDailyCommuteUsers/v1/', views.view_daily_commute_user_list),
    url(r'createDailyCommute/v1/', views.create_daily_commute),
    url(r'deleteDailyCommute/v1/', views.delete_daily_commute),
    ]