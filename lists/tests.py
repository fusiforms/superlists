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
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """
        Unit test that checks that home page redirects after a POST request
        """
        response = self.client.post('/', data={'item_text': 'A new list test item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list/')

    def test_only_saves_items_when_necessary(self):
        """
        Unit test to check that the database does not store item when the home page
        it visited, without the input field being filled
        """
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    """
    Unit tests for the list app's list view
    """
    def test_uses_list_template(self):
        """
        Unit test to check list view uses the correct template
        """
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        """
        Unit test to check list view page displays multiple items in a to-do list
        """
        Item.objects.create(text='My item one')
        Item.objects.create(text='My item 2')

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'My item one')
        self.assertContains(response, 'My item 2')


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
