"""
Unit tests for the lists app
"""
from django.test import TestCase

from lists.models import Item, List


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


class NewListTest(TestCase):
    """
    Unit tests for the list app's new list creation functionality
    """
    def test_can_save_a_post_request(self):
        """
        Unit test that checks that input box on the new list page saves with a POST request
        """
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """
        Unit test that checks that home page redirects after a POST request
        """
        response = self.client.post('/lists/new', data={'item_text': 'A new list test item'})
        self.assertRedirects(response, '/lists/the-only-list/')


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
        only_list = List.objects.create()
        Item.objects.create(text='My item one', list=only_list)
        Item.objects.create(text='My item 2', list=only_list)

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'My item one')
        self.assertContains(response, 'My item 2')


class ListAndItemModelsTest(TestCase):
    """
    Unit tests for the list app's item model and list model
    """
    def test_saving_and_retrieving_items(self):
        """
        Unit to test that list items can be saved and correctly retrieved
        """
        only_list = List()
        only_list.save()

        first_item = Item()
        first_item.text = 'The first list item'
        first_item.list = only_list
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.list = only_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, only_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(first_saved_item.list, only_list)
        self.assertEqual(second_saved_item.text, 'The second item')
        self.assertEqual(second_saved_item.list, only_list)
