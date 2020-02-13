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
from .models import DailyCommute
from .serializers import DailyCommuteSerializer
import logging
import socket
from django.forms.models import model_to_dict


@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["GET"])
def view_daily_commute_list(request):
    """
    This view should return the list of all daily commutes that user have configured.
    return: should return jouney_id (pk) of each list item of DailyCommute Model to be used by daily_commute_user_list view
    to fetch the list of user for a particular daily commute journey.
    """
    data = [
        {
            'jouney_id': 123,
            'title': 'Ghatkopar',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Trinity College Dublin, College Green'},
        {
            'jouney_id': 124,
            'title': 'Ghatkopar',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Spar, College Green'},
        {
            'jouney_id': 125,
            'title': 'Ghatkopar',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Trinity College Dublin, College Green'}, ]

    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def view_daily_commute_user_list(request):
    """
        This view should return the list of all daily commuters for the selected jouney_id
        input: journey_id (pk)
        return:  list of users that matched the given journey_id details
        to fetch the list of user for a particular daily commute journey.

        data = [
            {
                'first_name': alex,
                'gender': M
                'age': 20
                'Source': 'Dublin 8, Cork Street',
                'Destination': 'Trinity College Dublin, College Green'},
            {
                'first_name': alex,
                'gender': M
                'age': 20
                'Source': 'Dublin 8, Cork Street',
                'Destination': 'Trinity College Dublin, College Green'},
            {
                'first_name': alex,
                'gender': M
                'age': 20
                'Source': 'Dublin 8, Cork Street',
                'Destination': 'Trinity College Dublin, College Green'},
        ]
        """
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
                request.data.get('start_time') is None or request.data.get('journey_frequency') is None:
            return Response({'message': 'Form Data is missing!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        serializer = DailyCommuteSerializer(data=request.data)

        if serializer.is_valid():
            dailyCommuteDetails = serializer.save()
            dailyCommuteData = model_to_dict(dailyCommuteDetails,
                                 fields=['journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long', 'start_time', 'journey_frequency'])
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

