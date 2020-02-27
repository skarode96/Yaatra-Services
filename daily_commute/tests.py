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
from rest_framework.authtoken.models import Token
seed(1)
from .views import create_daily_commute

seed(1)

class create_user():
    def create_user(self, username, password, first_name, last_name, gender, email, pref_mode_travel, pref_gender, rating, total_rating_count,age):
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, gender=gender,
                                        age=age, email=email, password=password, rating=rating,
                                        total_rating_count=total_rating_count, pref_mode_travel=pref_mode_travel,
                                        pref_gender=pref_gender)
        user.set_password(password)
        user.save()
        auth_token, _ = Token.objects.get_or_create(user=user)
        return auth_token

class DailyCommuteTests(TestCase):
    """write daily commute tests: create, view, delete here"""

    username = randomString()
    password = randomString()


    def test_get_daily_commutes_for_user_with_no_schedules(self):
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
        user_id = response.data['userInfo']['id']
        user_id_body = {'user_id': user_id}
        response = self.client.post('/commute/daily/schedules/', user_id_body, HTTP_AUTHORIZATION='Token {}'.format(auth_token))
        self.assertTrue(response.status_code == HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_create_daily_commute_new_journey_id(self):
        """
        implement against view_daily_commute
        :return:
        """
        username = self.username
        password = self.password
        first_name = randomString()
        last_name = randomString()
        gender = randomString(1)
        email = Faker().email()
        pref_mode_travel = randint(0, 9)
        pref_gender = randint(0, 9)
        rating = randint(0, 5)
        total_rating_count = randint(20, 40)
        age = randint(0, 10)
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, gender=gender,
                                        age=age, email=email, password=password, rating=rating,
                                        total_rating_count=total_rating_count, pref_mode_travel=pref_mode_travel,
                                        pref_gender=pref_gender)
        user.set_password(password)
        user.save()
        auth_token, _ = Token.objects.get_or_create(user=user)

        # auth_token1 = create_user.create_user(self, username, password, first_name, last_name, gender, email, pref_mode_travel, pref_gender, rating, total_rating_count, age)
        credentials = {'username': self.username, 'password': self.password}
        response = self.client.post('/user/login/', credentials)
        auth_token = response.data['authToken']
        user_id = response.data['userInfo']['id']
        journey_details = {'journey_title': "office daily",
                           'source_long': "-6.0",
                           'source_lat': "53.0",
                            'destination_lat': "-6.02",
                           'destination_long': "53.03",
                           'start_time': "2020-02-13T15:05:11.621926Z",
                            'journey_frequency': "2",
                           'pref_mode_travel': pref_mode_travel,
                           'pref_gender': pref_gender,
                           'user_id':user_id}
        response = self.client.post('/commute/daily/', journey_details, HTTP_AUTHORIZATION='Token {}'.format(auth_token))
        print('response:', response.data)
        self.assertTrue(response.status_code == HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Journey creation Successful!')

        # def test_get_daily_commutes_for_user_with_schedules(self):
        #     print('----------------------',username1)
        #
        # def create_daily_commute_existing_journey_id(self):
        #     pass