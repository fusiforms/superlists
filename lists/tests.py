"""
Unit tests for the lists app
"""
from django.test import TestCase


class HomePageTest(TestCase):
    """
    Tests for the list app's home page
    """
    def test_uses_home_template(self):
        """
        Unit test to check that home page uses the correct home page template
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
