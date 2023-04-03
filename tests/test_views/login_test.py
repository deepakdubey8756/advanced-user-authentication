from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Profile
from utilities.genTokens import genToken
from account.forms import LoginForm


class LoginTestCase(TestCase):
    
    def setUp(self):

        #our client variable to manage current request and sessions.
        self.client = Client()

        #login url
        self.url = reverse('accounts:login')

        #user object on which we will test
        self.user = User.objects.create_user(username='testuser', email = 'testuser@gmail.com', password='RS22312/')
    

    # Check following cases:
    # 1. Check the case when user is already authenticated but profile is saved but not verfied.

    def test_nonverified_profile_authenticated(self):


        # this initial token will be store with inital non verified profile
        token = genToken()

        # our inintial non-verified profile....
        profile = Profile(user = self.user, token=token, isVerified=False)
        profile.save()

        # loging user before making request and checking if loging went successfull.
        self.assertTrue(self.client.login(username="testuser", password="RS22312/"))

        # testing response
        data = {'email':'testuser@gmail.com', 'password': 'RS22312/'}
        response = self.client.post(self.url, data)

        # testing response status
        self.assertEqual(response.status_code, 302)
        
        #testing if correct redirection happened
        self.assertRedirects(response, reverse('accounts:reset'))

        #checking if user is logged out or not 
        self.assertNotIn('_auth_user_id', self.client.session)

        
    # 2. Check case when user is authenticated and profile is also verified.
    def test_verified_profile_authentication(self):


        #creating initial logged in user with verified profile
        profile = Profile(user=self.user, token='None', isVerified=True)
        profile.save()

        # testified login to log user before testing on logged request.
        self.assertTrue(self.client.login(username="testuser", password="RS22312/"))

        #testing response
        response = self.client.post(self.url, {'username':'testuser', 'password': 'RS22312/'})

        # testing whether we get redirection response on not
        self.assertEqual(response.status_code, 302)
        
        # checking at which redirection happend
        self.assertRedirects(response, '/')

        # checking whether user is still logged in or not.
        self.assertIn('_auth_user_id', self.client.session)

    
    # 3. Testing the case when we send get request
    def test_get_request(self):

        # sending simple get request, this should return login form with template
        response = self.client.get(self.url)

        # checking response status
        self.assertEqual(response.status_code, 200)

        # checking correct template rendered
        self.assertTemplateUsed(response, 'registration/login.html')

        # checking corrent form rendered
        self.assertIsInstance(response.context['form'], LoginForm)


    # 4. Check case when we post request with wrong password.
    def test_login_with_wrong_password(self):

        # creating profile
        token = genToken()
        profile = Profile(user=self.user, token=token, isVerified=False)
        profile.save()

        # wrong password
        data = {'email':'testuser@gmail.com', 'password':'RS22312'}

        # sending wrong password
        response = self.client.post(self.url, data)

        # testing invalid error message
        self.assertContains(response, 'Wrong credentials')

        # testing returned template
        self.assertTemplateUsed(response, 'registration/login.html')

        # testing returned form
        self.assertIsInstance(response.context['form'], LoginForm)

    # 5. test login with wrong email
    def test_login_with_wrong_email(self):

        # wrong email
        data = {'email': 'testuser101@gmail.com', 'password': 'RS22312/'}

        # sending wrong email
        response = self.client.post(self.url, data)

        # testing invalid error message
        self.assertContains(response, 'User matching query does not exist.')

        # testing returned template
        self.assertTemplateUsed(response, 'registration/login.html')

        # testing returned form
        self.assertIsInstance(response.context['form'], LoginForm)

    # 6 . Check case when credentials is correct but profile is not verified.
    def test_login_with_non_verified_profile(self):

        # creating non verified account
        token = genToken()
        profile = Profile(user=self.user, token=token, isVerified=False)
        profile.save()

        # data
        data = {'email': 'testuser@gmail.com', 'password': 'RS22312/'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:reset"))

    # 5. Check the case when everything is fine and we have  a successful login.
    def test_login_successful(self):

        # creating verified profie
        profile = Profile(user=self.user, token="None", isVerified=True)
        profile.save()

        # data
        data = {'email': 'testuser@gmail.com', 'password': 'RS22312/'}
        response = self.client.post(self.url, data)

        # if successful then it should login user and redirect it to home page

        # check for redirection
        self.assertEqual(response.status_code, 302)

        # check for redirection at correct url
        self.assertRedirects(response, '/')

        # check for successful login
        self.assertIn('_auth_user_id', self.client.session)


    
