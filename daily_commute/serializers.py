from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

from user.models import User
from .models import DailyCommute


class DailyCommuteSerializer(serializers.ModelSerializer):
    permission_classes = (AllowAny,)

    class Meta:
        model = DailyCommute
        fields = ['user_id','journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long', 'start_time', 'pref_mode_travel', 'pref_gender', 'journey_frequency']

    def save(self):
        username = self.data.username
        dailyCommuteDetails = DailyCommute(journey_title=self.validated_data['journey_title'],
                           source_long=self.validated_data['source_long'],
                           source_lat=self.validated_data['source_lat'],
                           destination_lat=self.validated_data['destination_lat'],
                           destination_long=self.validated_data['destination_long'],
                           start_time=self.validated_data['start_time'],
                           journey_frequency=self.validated_data['journey_frequency'],
                           pref_gender =self.validated_data['pref_gender'],
                           pref_mode_travel=self.validated_data['pref_mode_travel'],
                           )
        user = User.objects.get(username= username)
        dailyCommuteDetails.user_id = user.pk
        dailyCommuteDetails.save()
        return dailyCommuteDetails

