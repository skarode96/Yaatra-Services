from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DailyCommute


class CustomUserAdmin(UserAdmin):
    list_display = (
        'pk', 'first_name', 'last_name', 'email', 'gender', 'age', 'username', 'created_on', 'last_login', 'password',
        'is_admin')
    search_fields = ('pk', 'email', 'username')
    readonly_fields = ('pk', 'created_on', 'last_login', 'password')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CustomDailyCommute(admin.ModelAdmin):
    list_display = (
        'user', 'journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long',
        'start_time', 'created_on')
    search_fields = ('journey_title',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(DailyCommute, CustomDailyCommute)
