from django.core.mail import outbox
from django.test import TestCase
from django.template.loader import render_to_string
from account.views import send_mail
from utilities.genTokens import genToken
import time

class SendMailTestCase(TestCase):
    def test_send_mail(self):
        token = genToken()
        # Test sending email with a valid email and domain
        user_email = "testuser@example.com"
        token = token
        template_str = "email_template.html"
        subject = "Test email"
        domain = "reset-password"
        
        status = send_mail(user_email, token, template_str, subject, domain)
        # time.sleep(4)
        print("This is my outbox")
        print(outbox)
        # Verify that the email was sent
        self.assertEqual(len(outbox), 1)
        self.assertEqual(outbox[0].subject, subject)
        self.assertEqual(outbox[0].to, [user_email])
        self.assertTrue(status['message_status'])
        
        # Verify that the email content is correct
        expected_content = render_to_string(template_str,{
            "token": token,
            "email": user_email,
            "protocol": "http",
            "domain": f"localhost:8000/accounts/{domain}"
        })
        self.assertIn(expected_content, outbox[0].body)
        
    # def test_send_mail_with_invalid_email(self):
    #     # Test sending email with an invalid email
    #     user_email = "invalid_email"
    #     token = "123456"
    #     template_str = "email_template.html"
    #     subject = "Test email"
    #     domain = "reset-password"
        
    #     response = send_mail(user_email, token, template_str, subject, domain)
        
    #     # Verify that the function returns the expected status and error message
    #     self.assertFalse(response["message_status"])
    #     self.assertIn("Invalid", response["message_content"])
        
    #     # Verify that no email was sent
    #     self.assertEqual(len(outbox), 0)
