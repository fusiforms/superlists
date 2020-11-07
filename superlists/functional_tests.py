"""
Functional test for superlists app (a To Do List)
"""
import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    """
    Class of TestCase to hold the function tests
    for a new visitor to the superlists site
    """

    def setUp(self):
        """
        Initiates the new visitor tests by attaching to the browser
        """
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """
        Finalise the new visitor tests by quitting the browser
        """
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        New visitor test that starts a new list, adds some items and
        verifies that the list can be found at itr URL
        """

        # Edith has heard about a new online to-do app.
        # She goes to the browser to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish writing the tests!')

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into a text box

        # When she hits enter, the page updates and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list.
        # She see some explanatory text noting that the sire has generated a unique URL for her.

        # She visits the URL and sees her to-do list is still there.

        # Satisfied, she goes to sleep.

if __name__ == '__main__':
    unittest.main()
