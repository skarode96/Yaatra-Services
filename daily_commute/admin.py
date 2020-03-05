from django.contrib import admin
from .models import DailyCommute


class CustomDailyCommute(admin.ModelAdmin):
    list_display = (
        'pk', 'user', 'journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long',
        'start_time', 'created_on', 'pref_gender', 'pref_mode_travel', 'journey_frequency', 'time_of_commute', 'journey_id')
    search_fields = ('journey_title', 'time_of_commute')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(DailyCommute, CustomDailyCommute)
