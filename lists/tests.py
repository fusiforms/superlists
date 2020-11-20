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
    def test_can_save_a_post_request_to_an_existing_list(self):
        """
        Unit test that checks that input box on the list page saves with a POST request
        """
        other_list = List.objects.create() # pylint: disable=unused-variable
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """
        Unit test that checks that adding an item to a list page redirects
        to the correct list view
        """
        other_list = List.objects.create() # pylint: disable=unused-variable
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new item for an existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')


class ListViewTest(TestCase):
    """
    Unit tests for the list app's list view
    """
    def test_uses_list_template(self):
        """
        Unit test to check list view uses the correct template
        """
        the_list = List.objects.create()
        response = self.client.get(f'/lists/{the_list.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        """
        Unit test to check list view page displays multiple items in a to-do list
        and only the items for a specific list
        """
        correct_list = List.objects.create()
        Item.objects.create(text='My item one', list=correct_list)
        Item.objects.create(text='My item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Your item 3', list=other_list)
        Item.objects.create(text='Your item 4', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'My item one')
        self.assertContains(response, 'My item 2')
        self.assertNotContains(response, 'Your item 3')
        self.assertNotContains(response, 'Your item 4')

    def test_passes_correct_list_to_template(self,):
        """
        Unit test to ensure that the correct list is passed in the context
        """
        other_list = List.objects.create() # pylint: disable=unused-variable
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


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
