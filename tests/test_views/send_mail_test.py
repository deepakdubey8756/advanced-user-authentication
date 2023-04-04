from django.core import mail
from django.test import TestCase
from django.template.loader import render_to_string
from account.views import send_mail
from utilities.genTokens import genToken
from django.conf import settings

class SendMailTestCase(TestCase):

    def test_sending_core_mail(self):

        token = genToken()
        user_email = "roloron703@dogemn.com"
        token = token
        template_str = "registration/email_templates.html"
        subject = "Test email confirmation"
        domain = "password_confirm"
        
        template = render_to_string(template_str,{
            "token": token,
            "email": user_email,
            "protocol": "http",
            "domain": f"localhost:8000/accounts/{domain}"
        })
        
        mail.send_mail(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently = False
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
       
      
