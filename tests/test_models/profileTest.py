from django.test import TestCase
from utilities.getUsername import getUsername
from django.contrib.auth.models import User
from account.models import Profile
from utilities.genTokens import genToken

#Testing different models
class ProfileTestCase(TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.email = "deepaktest@gmail.com"
        self.username = "deepaktest_gmail_com"
        self.password = "DeepakTestCase1233"


    def test_username_creation(self):
        print('Testing username creation')
        self.assertEqual(getUsername(self.email), "deepaktest_gmail_com")

    def test_user_creation(self):
        print("Testing user creation")
        user = User.objects.create_user(username=self.username, email = self.email, password = self.password)
        self.assertEqual(self.username, user.username)
        self.assertEqual(self.email, user.email)
        self.assertNotEqual(self.password, user.password)

    
    def test_profile(self):
        print("Testing profile creation")
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        token = genToken()
        profile = Profile(user=user, token=token, isVerified=False)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.token, token)
        self.assertEqual(profile.isVerified, False)
        

