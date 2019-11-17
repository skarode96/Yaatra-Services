from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class LogInTest(TestCase):

    def test_daily_commute_with_token(self):

        '''
        Testcase: To check access to Daily Commute Recommender API  endpoint with Authentication Token
        '''

        username = 'test'
        password = 'qwerty12340'
        user = User.objects.create_user(username)
        user.set_password(password)
        user.save()

        credentials = {'username': username, 'password': password}

        response = self.client.post('/login/v1/', credentials)
        token = response.data['token']
        self.assertTrue(response.status_code == 200, 'Login, API Testing: Failure')

        response = self.client.get('/dailycommute/v1/', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertTrue(response.status_code == 200, 'Daily Commute, API Testing: Failure')

'''
    def test_daily_commute_without_token(self):
    
        
        #Testcase: To check access to Daily Commute Recommender API endpoint without Authentication Token
        
        response = self.client.get('/dailycommute/v1/')
        print("API Response: ", response.data['detail'])
        self.assertTrue(response.status_code == 200, 'Daily Commute, API Testing: Failure')
'''