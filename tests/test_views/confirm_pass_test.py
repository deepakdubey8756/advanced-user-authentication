from django.test import TestCase, Client
from utilities.genTokens import genToken
from account.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse

class ConfirmPassTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='RS22312/')

    # Check following cases.
    # 1. Check when user is already authenticated.
    def test_when_user_authenticated(self):

        # loging user
        self.assertTrue(self.client.login(username='testuser', password='RS22312/'))

        # token to send for verification
        token = genToken()
        profile = Profile(user=self.user, token = token, isVerified=False)
        profile.save()

        # if user is already authenticated then it should authenticate to home page
        url = reverse('accounts:confirmPass', kwargs={'token': str(token)})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, '/')


    # 2. Check case when we have invalid token.
    def test_when_invalid_token(self):

        # saving token in profile
        token = genToken()
        profile = Profile(user=self.user, token = token, isVerified=False)
        profile.save()

        # sending wrong token 
        url = reverse('accounts:confirmPass', kwargs={'token': "Thisismywrongtoken"})

        response = self.client.get(url)

        # in case of wrong token it should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

    # 3. check case when we have a valid token.
    def test_with_valid_token(self):

        #creating profile to test
        token = genToken()
        profile = Profile(user = self.user, token=token, isVerified=False)
        profile.save()

        url = reverse('accounts:confirmPass', kwargs={'token': str(token)})

        response = self.client.get(url)
        
        # if token is correct then it should login user, update profile and redirect to home page
        # checking status code
        self.assertEqual(response.status_code, 302)

        # checking login 
        self.assertIn('_auth_user_id', self.client.session)

        # checking updated profile
        profile = Profile.objects.filter(user=self.user)
        self.assertEqual(len(profile), 1)
        self.assertEqual(profile[0].token, 'none')

        # checking if profile is verified.
        self.assertTrue(profile[0].isVerified)

        # check if request is redirected to home page
        self.assertRedirects(response, '/')


