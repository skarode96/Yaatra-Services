from django.test import TestCase
from .models import User, DailyCommute
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


class UserLoginTests(TestCase):
    """write user login tests here"""

    def test_user_login(self):
        username = randomString()
        password = randomString()
        firstname = randomString()
        lastname = randomString()
        gender = randomString(1)
        email = Faker().email()
        age = randint(0, 10)
        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, gender=gender,
                                        age=age, email=email, password=password)
        user.set_password(password)
        user.save()
        credentials = {'username': username, 'password': password}
        response = self.client.post('/backend/userLogin/v1/', credentials)
        self.assertTrue(response.status_code == HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login Successful!')

    def test_missing_username_password(self):
        credentials = {}
        response = self.client.post('/backend/userLogin/v1/', credentials)
        self.assertTrue(response.status_code == HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Either Username or Password is missing!')

    def test_invalid_username_password(self):
        credentials = {'username': randomString(), 'password': randomString()}
        response = self.client.post('/backend/userLogin/v1/', credentials)
        self.assertTrue(response.status_code == HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'User Not Found, Invalid Credentials!')


class UserRegistrationTests(TestCase):
    """write user registration tests here"""

    def test_missing_user_details(self):
        user_details = {}
        response = self.client.post('/backend/userRegister/v1/', user_details)
        self.assertTrue(response.status_code == HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Form Data is missing!')

    def test_user_register_login(self):
        password = randomString()
        user_details = {'username': randomString(), 'password': password, 'first_name': randomString(),
                        'last_name': randomString(), 'age': randint(0, 10), 'confirm_password': password,
                        'gender': randomString(1),'email': Faker().email()}
        response = self.client.post('/backend/userRegister/v1/', user_details)
        self.assertTrue(response.status_code == HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User Registration Successful!')


class DailyCommuteTests(TestCase):
    """write daily commute tests: create, view, delete here"""

    def test_view_daily_commute_with_token(self):
        username = randomString()
        password = randomString()
        firstname = randomString()
        lastname = randomString()
        gender = randomString(1)
        email = Faker().email()
        age = randint(0, 10)
        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, gender=gender,
                                        age=age, email=email, password=password)
        user.set_password(password)
        user.save()
        credentials = {'username': username, 'password': password}
        response = self.client.post('/backend/userLogin/v1/', credentials)
        token = response.data['auth_token']
        response = self.client.get('/backend/viewDailyCommutes/v1/', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertTrue(response.status_code == HTTP_200_OK)

    def test_daily_commute_without_token(self):
        token = ''
        response = self.client.get('/backend/viewDailyCommutes/v1/')
        self.assertTrue(response.status_code == HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
