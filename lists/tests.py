"""
Unit tests for the lists app
"""
from django.test import TestCase

class SmokeTest(TestCase):
    """
    Unit test that is guaranteed to fail
    """
    def test_bad_maths(self):
        """
        Maths test that will fail
        """
        self.assertEqual(1 + 1, 3)
