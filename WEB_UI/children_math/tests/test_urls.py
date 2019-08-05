from django.test import SimpleTestCase
from django.urls import reverse, resolve
from children_math.views import (children_math_main,
                                 children_math_01_task,
                                 children_math_02_task,
                                 children_math_02_result
                                 )


class TestUrls(SimpleTestCase):

    def test_children_math_main_resolves(self):
        url = reverse('children_math_main') # name from urls.py
        self.assertEqual(resolve(url).func, children_math_main) # imported

    def test_children_math_01_task_resolves(self):
        url = reverse('children_math_01_task') # name from urls.py
        self.assertEqual(resolve(url).func, children_math_01_task) # imported

    # def test_children_math_01_result_resolves(self):
    #     url = reverse('children_math_01_result') # name from urls.py
    #     self.assertEqual(resolve(url).func, children_math_01_result) # imported

    def test_children_math_02_task_resolves(self):
        url = reverse('children_math_02_task') # name from urls.py
        self.assertEqual(resolve(url).func, children_math_02_task) # imported

    def test_children_math_02_result_resolves(self):
        url = reverse('children_math_02_result') # name from urls.py
        self.assertEqual(resolve(url).func, children_math_02_result) # imported
