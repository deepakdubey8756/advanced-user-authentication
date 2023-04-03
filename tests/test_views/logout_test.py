from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Profile
from utilities.genTokens import genToken
from account.forms import LoginForm


class LogoutTestCase(TestCase):
    
    def setUp(self):

        # our client variable to manage current request and sessions.
        self.client = Client()

        # logout url
        self.url = reverse('accounts:logout')

        # user object on which we will test
        self.user = User.objects.create_user(username='testuser', email = 'testuser@gmail.com', password='RS22312/')
    

    # We will test following cases:
    # 1. test logout when user isn't logged in
    def test_logout_without_login(self):
        # sending response without loging in 
        response = self.client.post(self.url)
        
        # checking if redirected successfully
        self.assertEqual(response.status_code, 302)

        # checking if it is redirected to correct url
        self.assertRedirects(response, reverse('accounts:login') + '?next=' + self.url)
        
    # 2. test logout through get request
    def test_logout_through_get_request(self):
        # loging in 
        self.assertTrue(self.client.login(username='testuser', password="RS22312/"))

        # sending response without loging in 
        response = self.client.get(self.url)
        
        # checking if redirected successfully
        self.assertEqual(response.status_code, 302)

        # checking if it is redirected to correct url
        self.assertRedirects(response, '/')
        
    # 3. test logout through post request
    def test_logout_through_post_request(self):
         # loging in 
        self.assertTrue(self.client.login(username='testuser', password="RS22312/"))

        # sending response without loging in 
        response = self.client.post(self.url)
        
        # checking if redirected successfully
        self.assertEqual(response.status_code, 302)

        # checking if it is redirected to correct url
        self.assertRedirects(response, reverse("accounts:login"))

