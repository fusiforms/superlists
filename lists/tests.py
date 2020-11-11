"""
Unit tests for the lists app
"""
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """
    Test for the list app's home page
    """
    def test_root_url_resolves_to_home_page_view(self):
        """
        Unit test to check that the root URL can be resolved and
        calls the home_page view
        """
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        Unit test to chcek that home page returns html tags and a known title
        """
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do Lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
