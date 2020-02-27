from django.db import models
from django.conf import settings

class DailyCommute(models.Model):

    journey_title = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source_long = models.DecimalField(max_digits=9, decimal_places=6)
    source_lat = models.DecimalField(max_digits=9, decimal_places=6)
    destination_long = models.DecimalField(max_digits=9, decimal_places=6)
    destination_lat = models.DecimalField(max_digits=9, decimal_places=6)
    journey_frequency = models.IntegerField()
    pref_gender = models.IntegerField()
    pref_mode_travel = models.IntegerField()
    journey_id = models.IntegerField(default=0, editable=True)

    start_time = models.DateTimeField(verbose_name=' Journey Start Time')
    created_on = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True)

    REQUIRED_FIELDS = ['journey_id', 'journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long', 'start_time', 'journey_frequency', 'pref_mode_travel', 'pref_gender']

    def __str__(self):
        return self.journey_title
