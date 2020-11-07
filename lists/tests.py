"""
Unit tests for the lists app
"""
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
