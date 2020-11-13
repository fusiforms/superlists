"""
Functional test for superlists app (a To Do List)
"""
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    """
    LiveServerTestCase to hold the functional tests
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

    def check_for_row_in_list_table(self, row_text):
        """
        Helper function to check if supplied row text is in an HTML table with
        id 'id_list_table'
        """
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        New visitor test that starts a new list, adds some items and
        verifies that the list can be found at itr URL
        """

        # Edith has heard about a new online to-do app.
        # She goes to the browser to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box and hits Enter
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # When she hits enter, the page updates and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Edith wonders whether the site will remember her list.
        # She see some explanatory text noting that the sire has generated a unique URL for her.
        self.fail('Finish writing the tests!')

        # She visits the URL and sees her to-do list is still there.

        # Satisfied, she goes to sleep.