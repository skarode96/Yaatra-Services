from django.test import TestCase
from .models import User
from random import seed
from random import randint
from utils.utility import randomString
from faker import Faker
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
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
        first_name = randomString()
        last_name = randomString()
        gender = randomString(1)
        email = Faker().email()
        pref_mode_travel = randint(0, 9)
        pref_gender = randint(0, 9)
        age = randint(0, 10)

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, gender=gender,
                                        age=age, email=email, password=password, pref_mode_travel=pref_mode_travel, pref_gender=pref_gender)
        user.set_password(password)
        user.save()
        credentials = {'username': username, 'password': password}
        response = self.client.post('/user/login/', credentials)
        self.assertTrue(response.status_code == HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login Successful!')

    def test_missing_username_password(self):
        credentials = {}
        response = self.client.post('/user/login/', credentials)
        self.assertTrue(response.status_code == HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Either Username or Password is missing!')

    def test_invalid_username_password(self):
        credentials = {'username': randomString(), 'password': randomString()}
        response = self.client.post('/user/login/', credentials)
        self.assertTrue(response.status_code == HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'User Not Found, Invalid Credentials!')


class UserRegistrationTests(TestCase):
    """write user registration tests here"""

    def test_missing_user_details(self):
        user_details = {}
        response = self.client.post('/user/register/', user_details)
        self.assertTrue(response.status_code == HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Form Data is missing!')

    def test_user_register_login(self):
        password = randomString()
        user_details = {'username': randomString(), 'password': password, 'first_name': randomString(),
                        'last_name': randomString(), 'age': randint(0, 10), 'confirm_password': password,
                        'gender': randomString(1),'email': Faker().email(), 'pref_gender': randint(0, 9), 'pref_mode_travel': randint(0, 9)}
        response = self.client.post('/user/register/', user_details)
        self.assertTrue(response.status_code == HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User Registration Successful!')
