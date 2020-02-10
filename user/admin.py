from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        'pk', 'first_name', 'last_name', 'email', 'gender', 'age', 'username', 'created_on', 'last_login', 'password',
        'is_admin')
    search_fields = ('pk', 'email', 'username')
    readonly_fields = ('pk', 'created_on', 'last_login', 'password')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
