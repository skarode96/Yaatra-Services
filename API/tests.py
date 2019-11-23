from django.test import TestCase
from django.contrib.auth.models import User

import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class LogInTest(TestCase):

    def test_should_throw_400_username_password_missing(self):
        credentials = {}
        res = self.client.post('/login/v1/', credentials)
        self.assertTrue(res.status_code == 400)

    def test_should_throw_404_username_password_doesnt_exist(self):
        credentials = {'username':randomString(), 'password': randomString()}
        res = self.client.post('/login/v1/', credentials)
        self.assertTrue(res.status_code == 404)

    def test_daily_commute_with_token_should_give_200(self):
        username = randomString()
        password = randomString()
        user = User.objects.create_user(username)
        user.set_password(password)
        user.save()
        credentials = {'username': username, 'password': password}
        response = self.client.post('/login/v1/', credentials)
        token = response.data['token']
        response = self.client.get('/dailycommute/v1/', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertTrue(response.status_code == 200)


    def test_daily_commute_without_token_should_give_401(self):
        token=''
        response = self.client.get('/dailycommute/v1/', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertTrue(response.status_code == 401)
