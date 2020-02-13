import logging
import socket

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

from user.models import User
from .serializers import UserRegistrationSerializer
from utils.validator import validate_email, validate_username, validate_password


@ratelimit.decorators.ratelimit(key='ip', rate='20/h')
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(request):
    host_name = socket.gethostname()
    machine_ip = socket.gethostbyname(host_name)
    logger = logging.getLogger()
    logger.info("Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
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
        usr = User.objects.get(username=username)
        serializer = UserRegistrationSerializer(instance=usr)

        return Response({'message': 'Login Successful!',
                         'response': 'Success',
                         'authToken': auth_token.key,
                         'userInfo': serializer.data
                         },
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
                                     fields=['first_name', 'last_name', 'username', 'age', 'gender', 'email', 'pref_mode_travel', 'pref_gender'])
            userData['message'] = 'User Registration Successful!'
            userData['response'] = 'Success'
            auth_token = Token.objects.create(user=userDetails)
            userData['authToken'] = auth_token.key
        else:
            userData = serializer.errors
        return Response(userData, status=HTTP_201_CREATED)

