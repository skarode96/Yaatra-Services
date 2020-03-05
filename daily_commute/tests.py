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
    username2 = randomString()
    password2 = randomString()


    def test_get_daily_commutes_for_user_with_no_username(self):
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
        user_id_body = {'user_id': -1}
        response = self.client.post('/commute/daily/schedules/', user_id_body, HTTP_AUTHORIZATION='Token {}'.format(auth_token))
        self.assertEqual(response.data['message'],"User does not Exist!")


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

    def test_get_daily_commutes_schedules_by_userid(self):
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
        self.assertTrue(response.status_code == HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Journey creation Successful!')

        user_id_body = {'user_id': user_id}
        response = self.client.post('/commute/daily/schedules/', user_id_body, HTTP_AUTHORIZATION='Token {}'.format(auth_token))
        self.assertTrue(response.status_code == HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # def test_get_daily_commutes_schedules_by_journeyid(self):
    #     username = self.username
    #     password = self.password
    #     first_name = randomString()
    #     last_name = randomString()
    #     gender = randomString(1)
    #     email = Faker().email()
    #     pref_mode_travel = randint(0, 9)
    #     pref_gender = randint(0, 9)
    #     rating = randint(0, 5)
    #     total_rating_count = randint(20, 40)
    #     age = randint(0, 10)
    #     user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, gender=gender,
    #                                     age=age, email=email, password=password, rating=rating,
    #                                     total_rating_count=total_rating_count, pref_mode_travel=pref_mode_travel,
    #                                     pref_gender=pref_gender)
    #     user.set_password(password)
    #     user.save()
    #     auth_token, _ = Token.objects.get_or_create(user=user)
    #
    #     # auth_token1 = create_user.create_user(self, username, password, first_name, last_name, gender, email, pref_mode_travel, pref_gender, rating, total_rating_count, age)
    #     credentials = {'username': self.username, 'password': self.password}
    #     response = self.client.post('/user/login/', credentials)
    #     auth_token = response.data['authToken']
    #     user_id = response.data['userInfo']['id']
    #     journey_details = {'journey_title': "office daily",
    #                        'source_long': "-6.0",
    #                        'source_lat': "53.0",
    #                         'destination_lat': "-6.02",
    #                        'destination_long': "53.03",
    #                        'start_time': "2020-02-13T15:05:11.621926Z",
    #                         'journey_frequency': "2",
    #                        'pref_mode_travel': pref_mode_travel,
    #                        'pref_gender': pref_gender,
    #                        'user_id':user_id}
    #     response = self.client.post('/commute/daily/', journey_details, HTTP_AUTHORIZATION='Token {}'.format(auth_token))
    #     journey_id = response.data['journey_id']
    #     print("KKKKKK  ",journey_id,"  KKKKKKK  ",response.data)
    #     self.assertTrue(response.status_code == HTTP_201_CREATED)
    #     self.assertEqual(response.data['message'], 'Journey creation Successful!')
    #
    #     request_body = {'journey_id': journey_id,'user_id': user_id}
    #     response = self.client.post('/commute/daily/details/', request_body, HTTP_AUTHORIZATION='Token {}'.format(auth_token))
    #     print("PPPPPPPPP",response.data)
    #     self.assertTrue(response.status_code == HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)




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
        self.assertTrue(response.status_code == HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Journey creation Successful!')


    def test_create_daily_commute_new_journey_id_far(self):
        """
        implement against view_daily_commute
        :return:
        """
        user1_journey_id = -1;
        user2_journey_id = -1;

        username1 = self.username
        password1 = self.password
        first_name1 = randomString()
        last_name1 = randomString()
        gender1 = randomString(1)
        email1 = Faker().email()
        pref_mode_travel1 = randint(0, 9)
        pref_gender1 = randint(0, 9)
        rating1 = randint(0, 5)
        total_rating_count1 = randint(20, 40)
        age1 = randint(0, 10)
        user1 = User.objects.create_user(username=username1, first_name=first_name1, last_name=last_name1,
                                         gender=gender1,
                                         age=age1, email=email1, password=password1, rating=rating1,
                                         total_rating_count=total_rating_count1, pref_mode_travel=pref_mode_travel1,
                                         pref_gender=pref_gender1)
        user1.set_password(password1)
        user1.save()
        auth_token1, _ = Token.objects.get_or_create(user=user1)

        # auth_token1 = create_user.create_user(self, username, password, first_name, last_name, gender, email, pref_mode_travel, pref_gender, rating, total_rating_count, age)
        credentials1 = {'username': username1, 'password': password1}
        response = self.client.post('/user/login/', credentials1)
        auth_token1 = response.data['authToken']
        user_id1 = response.data['userInfo']['id']
        journey_details = {'journey_title': "office daily",
                           'source_long': "-6.0",
                           'source_lat': "53.0",
                           'destination_lat': "-6.02",
                           'destination_long': "53.03",
                           'start_time': "2020-02-13T15:05:11.621926Z",
                           'journey_frequency': "2",
                           'pref_mode_travel': pref_mode_travel1,
                           'pref_gender': pref_gender1,
                           'user_id': user_id1}
        response = self.client.post('/commute/daily/', journey_details,
                                    HTTP_AUTHORIZATION='Token {}'.format(auth_token1))
        self.assertTrue(response.status_code == HTTP_201_CREATED)
        user1_journey_id = response.data['journey_id']
        self.assertEqual(response.data['message'], 'Journey creation Successful!')

        username2 = self.username2
        password2 = self.password2
        first_name2 = randomString()
        last_name2 = randomString()
        gender2 = randomString(1)
        email2 = Faker().email()
        pref_mode_travel2 = randint(0, 9)
        pref_gender2 = randint(0, 9)
        rating2 = randint(0, 5)
        total_rating_count2 = randint(20, 40)
        age2 = randint(0, 10)
        user2 = User.objects.create_user(username=username2, first_name=first_name2, last_name=last_name2,
                                         gender=gender2,
                                         age=age1, email=email2, password=password2, rating=rating2,
                                         total_rating_count=total_rating_count2, pref_mode_travel=pref_mode_travel2,
                                         pref_gender=pref_gender2)
        user2.set_password(password2)
        user2.save()
        auth_token2, _ = Token.objects.get_or_create(user=user2)

        # auth_token1 = create_user.create_user(self, username, password, first_name, last_name, gender, email, pref_mode_travel, pref_gender, rating, total_rating_count, age)
        credentials2 = {'username': username2, 'password': password2}
        response = self.client.post('/user/login/', credentials2)
        auth_token2 = response.data['authToken']
        user_id2 = response.data['userInfo']['id']
        journey_details = {'journey_title': "office daily",
                           'source_long': "-6.0001",
                           'source_lat': "53.0001",
                           'destination_lat': "-6.02001",
                           'destination_long': "53.03001",
                           'start_time': "2020-02-13T15:05:11.621926Z",
                           'journey_frequency': "2",
                           'pref_mode_travel': pref_mode_travel2,
                           'pref_gender': pref_gender2,
                           'user_id': user_id2}
        response = self.client.post('/commute/daily/', journey_details,
                                    HTTP_AUTHORIZATION='Token {}'.format(auth_token2))
        self.assertTrue(response.status_code == HTTP_201_CREATED)
        user2_journey_id = response.data['journey_id']
        self.assertEqual(response.data['message'], 'Journey creation Successful!')

    def test_create_daily_commute_similar_journey_id(self):
            """
            implement against view_daily_commute
            :return:
            """
            user1_journey_id = -1;
            user2_journey_id = -1;

            username1 = self.username
            password1 = self.password
            first_name1 = randomString()
            last_name1 = randomString()
            gender1 = randomString(1)
            email1 = Faker().email()
            pref_mode_travel1 = randint(0, 9)
            pref_gender1 = randint(0, 9)
            rating1 = randint(0, 5)
            total_rating_count1 = randint(20, 40)
            age1 = randint(0, 10)
            user1 = User.objects.create_user(username=username1, first_name=first_name1, last_name=last_name1,
                                            gender=gender1,
                                            age=age1, email=email1, password=password1, rating=rating1,
                                            total_rating_count=total_rating_count1, pref_mode_travel=pref_mode_travel1,
                                            pref_gender=pref_gender1)
            user1.set_password(password1)
            user1.save()
            auth_token1, _ = Token.objects.get_or_create(user=user1)

            # auth_token1 = create_user.create_user(self, username, password, first_name, last_name, gender, email, pref_mode_travel, pref_gender, rating, total_rating_count, age)
            credentials1 = {'username': username1, 'password': password1}
            response = self.client.post('/user/login/', credentials1)
            auth_token1 = response.data['authToken']
            user_id1 = response.data['userInfo']['id']
            journey_details = {'journey_title': "office daily",
                               'source_long': "-6.0",
                               'source_lat': "53.0",
                               'destination_lat': "-6.02",
                               'destination_long': "53.03",
                               'start_time': "2020-02-13T15:05:11.621926Z",
                               'journey_frequency': "2",
                               'pref_mode_travel': pref_mode_travel1,
                               'pref_gender': pref_gender1,
                               'user_id': user_id1}
            response = self.client.post('/commute/daily/', journey_details,
                                        HTTP_AUTHORIZATION='Token {}'.format(auth_token1))

            self.assertTrue(response.status_code == HTTP_201_CREATED)
            user1_journey_id = response.data['journey_id']
            self.assertEqual(response.data['message'], 'Journey creation Successful!')

            journey_details = {'journey_title': "office daily",
                               'source_long': "-7.0",
                               'source_lat': "54.0",
                               'destination_lat': "-7.02",
                               'destination_long': "54.03",
                               'start_time': "2020-02-13T15:05:11.621926Z",
                               'journey_frequency': "2",
                               'pref_mode_travel': pref_mode_travel1,
                               'pref_gender': pref_gender1,
                               'user_id': user_id1}
            response = self.client.post('/commute/daily/', journey_details,
                                        HTTP_AUTHORIZATION='Token {}'.format(auth_token1))

            self.assertTrue(response.status_code == HTTP_201_CREATED)
            user1_journey_id = response.data['journey_id']
            self.assertEqual(response.data['message'], 'Journey creation Successful!')


