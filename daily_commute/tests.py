from django.test import TestCase
from user.models import User
from .models import DailyCommute
from random import seed
from random import randint
from utils.utility import randomString
from faker import Faker
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

seed(1)

class DailyCommuteTests(TestCase):
    """write daily commute tests: create, view, delete here"""

    def test_view_daily_commute_with_token(self):
        '''

        PASS USERNAME api NOT IMPLEMENTED

        username = randomString()
        password = randomString()
        first_name = randomString()
        last_name = randomString()
        gender = randomString(1)
        email = Faker().email()
        age = randint(0, 10)
        pref_mode_travel = randint(0, 9)
        pref_gender = randint(0, 9)
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, gender=gender,
                                        age=age, email=email, password=password, pref_mode_travel=pref_mode_travel, pref_gender=pref_gender)
        user.set_password(password)
        user.save()
        credentials = {'username': username, 'password': password}
        response = self.client.post('/user/login/', credentials)
        auth_token = response.data['authToken']
        response = self.client.get('/commute/daily/', HTTP_AUTHORIZATION='Token {}'.format(auth_token))
        self.assertTrue(response.status_code == HTTP_200_OK)
        '''
        pass

    def test_daily_commute_without_token(self):
        response = self.client.get('/commute/daily/')
        print(response)
        self.assertTrue(response.status_code == HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def create_daily_commute(self):
        """
        implement against view_daily_commute
        :return:
        """
        pass