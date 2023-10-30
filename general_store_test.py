import unittest
import HTMLTestRunner
import time
from appium import webdriver
import locators

# selenium imports
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# exceptions
from selenium.common.exceptions import ElementNotVisibleException

# locators
from locators import HomePage, ProductPage, CartPage, ProductPageLocators, CartPageLocators

capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='Android',
    # appPackage='com.androidsample.generalstore',
    # appActivity='com.androidsample.generalstore.MainActivity',
    # language='en',
    # locale='US'
)

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
        self.driver.implicitly_wait(50)
        self.homepage = HomePage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

        # wait - adding poll frequency and ignored exceptions
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException])

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_order(self):
        # having trouble launching the app normally so click on it
        el = self.driver.find_element(by=AppiumBy.XPATH,
                                      value='//android.widget.TextView[@content-desc="GeneralStore"]')
        el.click()
        time.sleep(3)

        # scroll to and select the country name
        self.homepage.select_country()

        # enter test user information (name and gender)
        self.homepage.enter_user_name()
        self.homepage.select_gender("F")

        # tap "Let's Shop" button
        self.homepage.click_shop_button()

        # verify that product screen is displayed
        self.assertEqual(self.product_page.get_text(*ProductPageLocators.PRODUCT_TITLE_BAR), "Products")

        # scroll down and add two items to cart
        for item_name in ProductPageLocators.ITEMS:
            added_item = self.product_page.add_item(item_name)
            self.assertEqual(added_item.text, item_name)
            time.sleep(1)

        # tap the cart button
        self.product_page.click_cart_button()

        # verify that the cart screen is displayed and that the correct items have been added
        self.assertEqual(self.product_page.get_text(*CartPageLocators.TITLE_BAR), "Cart")

        # verify that the total purchase amount is displayed (should be the sum of the prices of the two items added to the cart)
        total_cost = 0
        for item_name in ProductPageLocators.ITEMS:
            total_cost += self.cart_page.get_item_price(item_name)

        self.assertEqual(self.cart_page.get_purchase_price(), total_cost)

        # tap "Send me emails for discounts" checkbox
        self.cart_page.click_email_checkbox()

        # tap "Visit to website" button
        self.cart_page.click_proceed_button()

        time.sleep(3)

        # enter "General Store" in the search bar
        # need to switch contexts?
        webview = self.driver.contexts[1]
        self.driver.switch_to.context(webview)
        search_bar = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        search_bar.send_keys("General Store")
        time.sleep(3)

        # navigate back to the General Store app home screen
        self.driver.switch_to.context(self.driver.contexts[0])
        self.driver.back()

        # verify that the General Store home screen is displayed
        home_screen_title = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.androidsample.generalstore:id/toolbar_title")))
        self.assertEqual(home_screen_title.text, "General Store")

    def Store_Suite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestAppium("test_order"))
        return suite


if __name__ == '__main__':

    tests = TestAppium()

    runner = HTMLTestRunner.HTMLTestRunner(
        output='test_output',
        title='test_report',
        description='test report',
        open_in_browser=True,
    )
    runner.run(tests.Store_Suite())
    # unittest.main(testRunner=runner)
