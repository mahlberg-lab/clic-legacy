# -*- coding: utf-8 -*-
'''
This test suite can also be used to load the cache of frequent search options.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


"""
What are the tests we need?

The following corpora:
- all dickens
- all ntc
- all
- a few specific books

The following subcorpora:
- whole text
- quotes
- non-quotes
- long suspensions
- short suspensions

The following search options:

- Whole phrase
- Any


The options are:
{'corpus': ['BH', 'OT', 'dickens', 'ntc', 'all'],
 'search_mode': ['phrase', 'or'],
 'search_terms': ['dense fog', 'fog', 'the', 'we', 'he said', 'manner voice tone'],
 'subset': ['whole', 'quotes', 'non-quotes', 'long sus', 'short sus']}

combinations = [dict(zip(options, prod)) for prod in product(*(options[option] for option in options))]

[{'corpus': 'BH',
  'search_mode': 'phrase',
  'search_terms': 'dense fog',
  'subset': 'whole'},
 {'corpus': 'BH',
  'search_mode': 'phrase',
  'search_terms': 'fog',
  'subset': 'whole'},
  ...

"""


class FogInAllDickensWholePhrase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://clic.nottingham.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_fog_in_all_dickens_whole_phrase(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Concordance").click()
        driver.find_element_by_id("concordanceSearch").clear()
        driver.find_element_by_id("concordanceSearch").send_keys("fog")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("1 to 94 of 94 entries", driver.find_element_by_id("dataTableConcordance_info").text)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class FogInAllDickensAny(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://clic.nottingham.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_fog_in_all_dickens_any(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Concordance").click()
        driver.find_element_by_id("concordanceSearch").clear()
        driver.find_element_by_id("concordanceSearch").send_keys("fog")
        driver.find_element_by_id("any").click()
        driver.find_element_by_xpath("//label[2]").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("1 to 94 of 94 entries", driver.find_element_by_id("dataTableConcordance_info").text)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class MaybeInAllDickensWholePhraseQuotes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://clic.nottingham.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_maybe_in_all_dickens_whole_phrase_quotes(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Concordance").click()
        driver.find_element_by_id("concordanceSearch").clear()
        driver.find_element_by_id("concordanceSearch").send_keys("maybe")
        driver.find_element_by_id("testIdxMod2").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("1 to 45 of 45 entries", driver.find_element_by_id("dataTableConcordance_info").text)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class MaybeWhyInAllDickensAnyQuotes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://clic.nottingham.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_maybe_why_in_all_dickens_any_quotes(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Concordance").click()
        driver.find_element_by_id("concordanceSearch").clear()
        driver.find_element_by_id("concordanceSearch").send_keys("maybe why")
        driver.find_element_by_id("any").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_id("dataTableConcordance_info")
        #driver.find_element_by_css_selector("#sizzle-1422464805938 > img").click()
        #driver.find_element_by_css_selector("div.gradient-black-transparent.transition").click()
        # Warning: verifyTextNotPresent may require manual changes
        #try: self.assertNotRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        #except AssertionError as e: self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class TheInBleakHouseNonQuotesWholePhrase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://clic.nottingham.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_the_in_bleak_house_non_quotes_whole_phrase(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Concordance").click()
        driver.find_element_by_id("testIdxMod3").click()
        driver.find_element_by_link_text("Change books").click()
        driver.find_element_by_id("allDickensChk").click()
        driver.find_element_by_css_selector("#otherChk > div.checkbox > label > input[name=\"testCollection\"]").click()
        driver.find_element_by_id("booksModalSubmit").click()
        driver.find_element_by_id("concordanceSearch").clear()
        driver.find_element_by_id("concordanceSearch").send_keys("the")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_id("dataTableConcordance_info")
        # Warning: verifyTextNotPresent may require manual changes
        #try: self.assertNotRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        #except AssertionError as e: self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class YouInNonDickensNonQuotesWholePhrase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://clic.nottingham.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_you_in_non_dickens_non_quotes_whole_phrase(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Concordance").click()
        driver.find_element_by_id("concordanceSearch").clear()
        driver.find_element_by_id("concordanceSearch").send_keys("you")
        driver.find_element_by_id("testIdxMod3").click()
        driver.find_element_by_link_text("Change books").click()
        driver.find_element_by_id("allNtcChk").click()
        driver.find_element_by_id("allDickensChk").click()
        driver.find_element_by_css_selector("button.close").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_id("dataTableConcordance_info")
        # Warning: verifyTextNotPresent may require manual changes
        #try: self.assertNotRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        #except AssertionError as e: self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class CouldShouldInAllDickensAnyWholeText(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://clic.nottingham.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_could_should_in_all_dickens_any_whole_text(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text("Concordance").click()
        driver.find_element_by_id("concordanceSearch").clear()
        driver.find_element_by_id("concordanceSearch").send_keys("could should")
        driver.find_element_by_id("any").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_id("dataTableConcordance_info")
        #driver.find_element_by_css_selector("#sizzle-1422464805938 > img").click()
        #driver.find_element_by_css_selector("div.gradient-black-transparent.transition").click()
        # Warning: verifyTextNotPresent may require manual changes
        #try: self.assertNotRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*$")
        #except AssertionError as e: self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
