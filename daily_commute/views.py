from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
import ratelimit.decorators

from user.models import User
from utils.validator import validate_email, validate_username
from .models import DailyCommute
from .serializers import DailyCommuteSerializer
import logging
import socket
from django.forms.models import model_to_dict


@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["GET"])
def get_daily_commutes_for_user(request, user_id):
    """
    This view should return the list of all daily commutes that user have configured.
    return: should return jouney_id (pk) of each list item of DailyCommute Model to be used by daily_commute_user_list view
    to fetch the list of user for a particular daily commute journey.
    """
    data = [
        {
            'journey_id': 123,
            'title': 'office daily',
            'source_lat': 34.55,
            'source_long': 35.66,
            'destination_lat': 67.55,
            'destination_long': 45.66,
            'journey_frequency': 1,
            'pref_gender': 2,
            'pref_mode_travel': 2

        },
        {
            'journey_id': 211,
            'title': 'Gym daily',
            'source_lat': 34.55,
            'source_long': 35.66,
            'destination_lat': 67.55,
            'destination_long': 45.66,
            'journey_frequency': 1,
            'pref_gender': 2,
            'pref_mode_travel': 2
        }
    ]

    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_user_list_for_journey(request, journey_id):
    """
        This view should return the list of all daily commuters for the selected jouney_id
        input: journey_id (pk)
        return:  list of users that matched the given journey_id details
        to fetch the list of user for a particular daily commute journey.
    """
    data = [
            {
                'first_name': 'alex',
                'gender': 'M',
                'age': 20,
                'Source': 23.66,
                'Destination': 34.66},
            {
                'first_name': 'alex',
                'gender': 'M',
                'age': 20,
                'Source': 23.66,
                'Destination': 34.66},
            {
                'first_name': 'alex',
                'gender': 'M',
                'age': 20,
                'Source': 23.66,
                'Destination': 34.66},
        ]

    data = []
    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def create_daily_commute(request):
    """
    Input: Journey Details: longitude, latitude, start_time
    """
    if request.method == 'POST':

        if request.data.get('journey_title') is None or request.data.get('destination_lat') is None or \
                request.data.get('start_time') is None or request.data.get('journey_frequency') is None or request.data.get('username') is None:
            return Response({'message': 'Form Data is missing!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        username = request.data.get('username')
        if validate_username(username) is None:
            return Response({'message': 'Username does not Exist!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)


        serializer = DailyCommuteSerializer(data=request.data)

        if serializer.is_valid():
            dailyCommuteDetails = serializer.save()
            dailyCommuteData = model_to_dict(dailyCommuteDetails,
                                 fields=['user_id', 'journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long', 'start_time', 'journey_frequency'])
            dailyCommuteData['message'] = 'User Registration Successful!'
            dailyCommuteData['response'] = 'Success'
        else:
            userData = serializer.errors
        return Response(userData, status=HTTP_201_CREATED)

@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["DELETE"])
@permission_classes((AllowAny,))
def delete_daily_commute(request):
    """
    Input: Journey Details: journey_id
    """
    data = []
    return Response(data, status=HTTP_200_OK)

