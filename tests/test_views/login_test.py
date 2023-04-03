from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Profile
from utilities.genTokens import genToken
from django.contrib.auth import login, logout


class LoginTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:login')
        self.user = User.objects.create_user(username='testuser', password='MYd800999/')
    
    # Check following cases:
    # 1. Check case when user is already authenticated and profile is saved but not verfied.
    def test_nonverified_profile_authenticated(self):

        # creating inintial logged in user with non-verified profile
        token = genToken()
        profile = Profile(user = self.user, token=token, isVerified=False)
        profile.save()
        self.assertTrue(self.client.login(username="testuser", password="MYd800999/"))

        #testing response
        response = self.client.post(self.url, {'username':'testuser', 'password': 'MYd800999/'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:reset'))
        self.assertNotIn('_auth_user_id', self.client.session)
        

    def test_verified_profile_authentication(self):
        pass

    # 2. Check case when user is authenticated and profile is also verified.
    # 2.5: Check case when we get GET-REQUEST. 
    # 3. Check case when we post request with wrong credentials.
    # 4. Check case when credentials is correct but profile is not verified.
    # 5. Check the case when everything is fine and we have  a successful login.


    
