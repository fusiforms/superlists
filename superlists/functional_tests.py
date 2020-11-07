"""
Initial functional test for TDD
"""
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('http://localhost:8000')

# browser.maximize_window()
# browser.get('https://www.google.com/')
# browser.find_element_by_name('q').send_keys('morning')
# browser.find_element_by_name('q').send_keys(Keys.ENTER)
# browser.close()
# print("Sample test case run, and browser closed.")

assert 'Django' in browser.title
