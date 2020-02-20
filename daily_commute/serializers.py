from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from .models import DailyCommute


class DailyCommuteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyCommute
        fields = ['user_id', 'journey_id', 'journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long', 'start_time', 'pref_mode_travel', 'pref_gender', 'journey_frequency']

    def save(self):
        dailyCommuteDetails = DailyCommute(journey_title=self.validated_data['journey_title'],
                           user=self.validated_data['user_id'],
                           source_long=self.validated_data['source_long'],
                           source_lat=self.validated_data['source_lat'],
                           destination_lat=self.validated_data['destination_lat'],
                           destination_long=self.validated_data['destination_long'],
                           start_time=self.validated_data['start_time'],
                           journey_frequency=self.validated_data['journey_frequency'],
                           pref_gender =self.validated_data['pref_gender'],
                           pref_mode_travel=self.validated_data['pref_mode_travel'],
                           journey_id=self.validated_data['journey_id']
                           )
        dailyCommuteDetails.save()
        return dailyCommuteDetails

