from datetime import datetime, timedelta
from decimal import Decimal
import datetime as dt

from django.db.models import Max, Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from user.models import User
from user.serializers import UserRegistrationSerializer
from utils.validator import validate_username, validate_journey, validate_user_id
import ratelimit.decorators
from .models import DailyCommute
from .serializers import DailyCommuteSerializer
import logging
import socket
from django.forms.models import model_to_dict
import mpu

host_name = socket.gethostname()
machine_ip = socket.gethostbyname(host_name)


@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["POST"])
def get_daily_commutes_for_user(request):
    logger = logging.getLogger()
    logger.info("Get-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
    This view should return the list of all daily commutes that user have configured.
    return: should return jouney_id (pk) of each list item of DailyCommute Model to be used by daily_commute_user_list view
    to fetch the list of user for a particular daily commute journey.
    """

    if request.method == 'POST':
        user_id = request.user.pk

        if validate_user_id(user_id) is None:
            return Response({'message': 'User is not valid!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user_id = user.pk
        daily_commutes = DailyCommute.objects.filter(user_id=user_id)
        serializer = DailyCommuteSerializer(instance=daily_commutes, many=True)
        data = serializer.data[:]
        for detail in data:
            journey_id = detail.get('journey_id')
            detail['number_of_travellers'] = DailyCommute.objects.filter(journey_id=journey_id).count()
        response = {
            'message': 'Journey fetching successful!',
            'response': 'Success',
            'journey_details': data
        }
        return Response(response, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["POST"])
def get_journey_details(request):
    logger = logging.getLogger()
    logger.info(
        "User-List-for-Journey: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
        This view should return the list of all daily commuters for the selected jouney_id
        input: journey_id (pk)
        return:  list of users that matched the given journey_id details
        to fetch the list of user for a particular daily commute journey.
        """
    if request.method == 'POST':

        if request.data.get('journey_title') is None:
            return Response({'message': 'Form Data is missing!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        journey_id = request.data.get('journey_id')
        user_id = request.user.pk

        if validate_user_id(user_id) is None:
            return Response({'message': 'User is not valid!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        if validate_journey(journey_id) is None:
            return Response({'message': 'Journey does not exist!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user_id = user.pk
        user_details = []
        daily_commutes = DailyCommute.objects.filter(journey_id=journey_id)
        if daily_commutes:
            for commute in daily_commutes:
                User.objects.only('gender')
                details = User.objects.get(id=commute.user_id)
                user_details_serializer = UserRegistrationSerializer(instance=details)
                user_data = user_details_serializer.data
                user_data['source_lat'] = commute.source_lat
                user_data['source_long'] = commute.source_long
                user_data['destination_lat'] = commute.destination_lat
                user_data['destination_long'] = commute.destination_long
                user_data['time_of_commute'] = commute.time_of_commute
                user_data['commute_start_date'] = commute.start_time
                user_details.append(user_data)

        commute_detail = DailyCommute.objects.get(journey_id=journey_id, user=user_id)
        serializer = DailyCommuteSerializer(commute_detail)
        data = serializer.data
        data['traveller_info'] = user_details
        data['message'] = 'Journey details fetch successful'
        data['response'] = 'Success'
        return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["GET"])
def daily_commuter_notification(request):
    logger = logging.getLogger()
    logger.info(
        "Create-Daily-Notification: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
    Input: Notification   """
    data = []
    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["POST"])
def create_daily_commute(request):
    """
    Input: Journey Details: longitude, latitude, start_time
    """
    logger = logging.getLogger()
    logger.info("Create-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    if request.method == 'POST':

        if request.data.get('journey_title') is None or request.data.get('source_long') is None or \
                request.data.get('source_lat') is None or request.data.get('destination_lat') is None or \
                request.data.get('destination_long') is None or request.data.get('journey_frequency') is None or \
                request.data.get('start_time') is None or request.data.get('pref_mode_travel') is None or \
                request.data.get('time_of_commute') is None or request.data.get('pref_gender') is None:
            return Response({'message': 'Form Data is missing!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        user_id = request.user.pk
        if validate_user_id(user_id) is None:
            return Response({'message': 'User is not valid!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        user = User.objects.get(id=user_id)
        data['user'] = user.pk
        source_long, source_lat = request.data.get('source_long'), request.data.get('source_lat')
        dest_long, dest_lat = request.data.get('destination_long'), request.data.get('destination_lat')
        freq = request.data.get('journey_frequency')
        time = datetime.strptime(request.data.get('time_of_commute'), '%H:%M:%S')

        latlong_km = Decimal(0.0039)
        buffer_time = timedelta(minutes=5)

        max_buffer = (time+buffer_time).timetuple()
        min_buffer = (time-buffer_time).timetuple()
        source_long_min, source_long_max = Decimal(source_long) - latlong_km, Decimal(source_long) + latlong_km
        source_lat_min, source_lat_max = Decimal(source_lat) - latlong_km, Decimal(source_lat) + latlong_km
        dest_long_min, dest_long_max = Decimal(dest_long) - latlong_km, Decimal(dest_long) + latlong_km
        dest_lat_min, dest_lat_max = Decimal(dest_lat) - latlong_km, Decimal(dest_lat) + latlong_km
        nearby_travels = DailyCommute.objects.exclude(user=user.pk).filter(source_lat__lte=source_lat_max, source_lat__gte=source_lat_min,
                                                     source_long__lte=source_long_max, source_long__gte=source_long_min,
                                                     destination_lat__lte=dest_lat_max,
                                                     destination_lat__gte=dest_lat_min,
                                                     destination_long__lte=dest_long_max,
                                                     destination_long__gte=dest_long_min,
                                                     journey_frequency=freq,
                                                     time_of_commute__lte=dt.time(max_buffer[3],max_buffer[4],max_buffer[5]),
                                                     time_of_commute__gte=dt.time(min_buffer[3],min_buffer[4],min_buffer[5]),
                                                     )
        serializer = DailyCommuteSerializer(instance=nearby_travels, many=True)
        nearby_travel_data = serializer.data[:]
        if nearby_travels:
            # other_nearby_travellers = QuerySet.filter(~Q(user=user.pk))
            minimum_distance = 1000
            for travel in nearby_travels:
                distance = mpu.haversine_distance((Decimal(travel.source_lat), Decimal(travel.source_long)), (Decimal(source_lat), Decimal(source_long)))
                if distance < minimum_distance:
                    minimum_distance = distance
                    data['journey_id'] = travel.journey_id
        else:
            if DailyCommute.objects.all().exists():
                max_journey_id = DailyCommute.objects.all().aggregate(Max('journey_id'))['journey_id__max'] + 1
            else:
                max_journey_id = 0
            data['journey_id'] = max_journey_id
        data['user'] = user.pk
        serializer = DailyCommuteSerializer(data=data)
        if serializer.is_valid():
            dailyCommuteDetails = serializer.save()
            dailyCommuteData = model_to_dict(dailyCommuteDetails,
                                             fields=['journey_id', 'journey_title', 'source_long', 'source_lat', 'destination_lat',
                                                     'destination_long', 'journey_frequency'])
            dailyCommuteData['message'] = 'Journey creation Successful!'
            dailyCommuteData['response'] = 'Success'
        else:
            dailyCommuteData = serializer.errors
        return Response(dailyCommuteData, status=HTTP_201_CREATED)

@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["DELETE"])
def delete_daily_commute(request):
    """
    Input: Journey Details: journey_id
    """
    logger = logging.getLogger()
    logger.info("Delete-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    data = []
    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["PUT"])
def update_daily_commute(request):
    logger = logging.getLogger()
    logger.info("Update-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
    Input: Journey Details: journey_id
    """
    data = []
    return Response(data, status=HTTP_200_OK)
