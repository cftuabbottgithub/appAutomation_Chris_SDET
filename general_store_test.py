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
import locators

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
        country_select = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.androidsample.generalstore:id/spinnerCountry")))
        country_select.click()
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                 f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{locators.COUNTRY_NAME}"))')
        country_select_entry = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, f"//android.widget.TextView[@text='{locators.COUNTRY_NAME}']")))
        country_select_entry.click()

        # enter test user information (name and gender)
        user_entry = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.androidsample.generalstore:id/nameField")))
        user_entry.send_keys(f"{locators.USER_NAME}")
        gender_entry_f = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.androidsample.generalstore:id/radioFemale")))
        gender_entry_f.click()

        # tap "Let's Shop" button
        lets_shop_button = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.androidsample.generalstore:id/btnLetsShop")))
        lets_shop_button.click()

        # verify that product screen is displayed
        product_title_bar = self.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[@text='Products']")))
        self.assertEqual(product_title_bar.text, "Products")

        # scroll down and add two items to cart
        for item_name in locators.ITEMS:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                     f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{item_name}"))')
            item_el = self.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, f"//android.widget.TextView[@text='{item_name}']")))
            self.assertEqual(item_el.text, item_name)

            # add item to cart
            add_item_layout = self.driver.find_element(AppiumBy.XPATH,
                                                       f"//android.widget.TextView[@text='{item_name}']/following-sibling::android.widget.LinearLayout[2]")
            add_item_button = add_item_layout.find_element(AppiumBy.XPATH,
                                                           "//android.widget.TextView[@text='ADD TO CART']")
            self.assertEqual(add_item_button.text, "ADD TO CART")
            add_item_button.click()
            time.sleep(1)

        # tap the cart button
        cart_button = self.driver.find_element(AppiumBy.ID, "com.androidsample.generalstore:id/appbar_btn_cart")
        cart_button.click()

        # verify that the cart screen is displayed and that the correct items have been added
        cart_title_bar = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.androidsample.generalstore:id/toolbar_title")))
        self.assertEqual(cart_title_bar.text, "Cart")

        # verify that the total purchase amount is displayed (should be the sum of the prices of the two items added to the cart)
        total_cost = 0
        for item_name in locators.ITEMS:
            # look for the price
            price_layout = self.driver.find_element(AppiumBy.XPATH,
                                                    f"//android.widget.TextView[@text='{item_name}']/following-sibling::android.widget.LinearLayout[2]")
            price = price_layout.find_element(AppiumBy.XPATH, "//android.widget.TextView")
            total_cost += float(price.text[1:])

        total_purchase_amount = self.driver.find_element(AppiumBy.XPATH,
                                                         f"//android.widget.TextView[@text='Total Purchase Amount:  ']/following-sibling::android.widget.TextView[1]")
        total_purchase_amount = float(total_purchase_amount.text[1:])

        self.assertEqual(total_purchase_amount, total_cost)

        # tap "Send me emails for discounts" checkbox
        email_checkbox = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,
                                                                         "//android.widget.CheckBox[@text='Send me e-mails on discounts related to selected products in future']")))
        email_checkbox.click()

        # tap "Visit to website" button
        website_button = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.androidsample.generalstore:id/btnProceed")))
        website_button.click()

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
