"""
Unit tests for the lists app
"""
from django.test import TestCase

from lists.models import Item


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

    def test_can_save_a_post_request(self):
        """
        Unit test that checks that input box on the home page saves with a POST request
        """
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')


class ItemModelTest(TestCase):
    """
    Unit tests for the list app's item model
    """
    def test_saving_and_retrieving_items(self):
        """
        Unit to test that list items can be saved and correctly retrieved
        """
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'The second item')
