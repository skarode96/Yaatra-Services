from django.shortcuts import render

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))

def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Either Username or Password is missing!'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'User Not Found, Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def daily_commute_recommender(request):
    data = [
        {
            'User': 'Kevin',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Trinity College Dublin, College Green'},
        {
            'User': 'Richard',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Spar, College Green'},
        {
            'User': 'John',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Trinity College Dublin, College Green'}, ]

    return Response(data, status=HTTP_200_OK)