from django.test import TestCase
from account.views import extract_email_details
from django.contrib.auth.models import User
from utilities.getUsername import getUsername
class ExtractEmailDetailsTestCase(TestCase):

    def test_user_does_not_exist(self):
        request_dict = {"email": "johndoe@example.com", "password": "testpassword", "confirmPass": "testpassword"}

        result = extract_email_details(request_dict)

        self.assertTrue(result['status'])
        self.assertEqual(result['message_content'], 'Everything is fine')
        self.assertEqual(result['username'], 'johndoe_example_com')

    def test_user_exists(self):

        User.objects.create_user(username= getUsername("johndoe@example.com"), email="johndoe@example.com", password="testpassword")

        # Create a request dictionary with the same email, password, and confirmPass values as the existing user
        request_dict = {"email": "johndoe@example.com", "password": "testpassword", "confirmPass": "testpassword"}

        # Call the extract_email_details() function
        result = extract_email_details(request_dict)

        # Check that the status is False and the message_content is "Account already exists"
        self.assertFalse(result['status'])
        self.assertEqual(result['message_content'], 'Account already exits')
