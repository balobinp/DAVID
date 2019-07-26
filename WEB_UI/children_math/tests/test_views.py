from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_children_math_main_GET(self):
        response = self.client.get(reverse('children_math_main')) # name from urls.py
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/children_math/')