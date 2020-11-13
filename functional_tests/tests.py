"""
Functional test for superlists app (a To Do List)
"""
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


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

    def wait_for_row_in_list_table(self, row_text):
        """
        Helper function to check if supplied row text is in an HTML table with
        id 'id_list_table' and retrying up to a maxiumm wait time.
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        """
        New visitor test that starts a new list, adds some items and
        verifies that the list can be found at its URL
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

        # When she hits enter, the page updates and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Satisfied, she goes to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """
        New visitor test that starts two lists (for two different users),
        adds some items and verifies that the lists can be found at their URLs
        and that there is no sharing of items between urls.
        """

        # Edith starts a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy goose feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy goose feathers')

        # Edith notes that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # A new user, Frances, comes along to the site
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Frances vists the home page. There is no sign of Edith's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy goose feathers', page_text)
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # Frances starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Frances notes that her list has its own unique URL
        frances_list_url = self.browser.current_url
        self.assertRegex(frances_list_url, '/lists/.+')
        self.assertNotEqual(frances_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy goose feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
