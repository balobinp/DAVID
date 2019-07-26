from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mainpage.views import index


class TestUrls(SimpleTestCase):

    def test_main_url_resolves(self):
        url = reverse('mainpage')
        self.assertEqual(resolve(url).func, index)