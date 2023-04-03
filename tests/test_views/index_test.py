from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class IndexViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:index')
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_index_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/index.html')
    
    def test_index_view_with_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('accounts:login') + '?next=' + self.url)
