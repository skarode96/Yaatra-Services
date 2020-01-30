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
from django.forms.models import model_to_dict
from .serializers import UserRegistrationSerializer
from utils.validator import validate_email, validate_username, validate_password


@ratelimit.decorators.ratelimit(key='ip', rate='20/h')
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(request):
    if request.method == 'POST':

        if request.data.get("username") is None or request.data.get("password") is None:
            return Response({'message': 'Either Username or Password is missing!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'message': 'User Not Found, Invalid Credentials!',
                             'response': 'Error'},
                            status=HTTP_404_NOT_FOUND)

        auth_token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login Successful!',
                         'response': 'Success',
                         'authToken': auth_token.key},
                        status=HTTP_200_OK)
    else:
        return Response({'message': 'Use Post Request!',
                         'response': 'Error'},
                        status=HTTP_400_BAD_REQUEST)


@ratelimit.decorators.ratelimit(key='ip', rate='20/h')
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_registration(request):
    if request.method == 'POST':

        if request.data.get('email') is None or request.data.get('username') is None or \
                request.data.get('first_name') is None or request.data.get('gender') is None or request.data.get(
            'age') is None or request.data.get('last_name') is None \
                or request.data.get('password') is None or request.data.get('confirm_password') is None:
            return Response({'message': 'Form Data is missing!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        email = request.data.get('email').lower()
        if validate_email(email) is not None:
            return Response({'message': 'Email Already Exists!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        username = request.data.get('username')
        if validate_username(username) is not None:
            return Response({'message': 'Username Already Exists!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        if validate_password(request.data.get('password'), request.data.get('confirm_password')) is None:
            return Response({'message': 'Password Mismatched!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            userDetails = serializer.save()
            userData = model_to_dict(userDetails,
                                     fields=['first_name', 'last_name', 'username', 'age', 'gender', 'email'])
            userData['message'] = 'User Registration Successful!'
            userData['response'] = 'Success'
            auth_token = Token.objects.create(user=userDetails)
            userData['authToken'] = auth_token.key
        else:
            userData = serializer.errors
        return Response(userData, status=HTTP_201_CREATED)


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
def create_daily_commute(request):
    """
    Input: Journey Details: longitude, latitude, start_time
    """
    data = []
    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["DELETE"])
def delete_daily_commute(request):
    """
    Input: Journey Details: journey_id
    """
    data = []
    return Response(data, status=HTTP_200_OK)
