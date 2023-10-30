from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver

# selenium imports
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from appium.options.common import AppiumOptions

# exceptions
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, \
    ElementClickInterceptedException


class HomeScreenLocators(object):
    # home screen parameters
    COUNTRY_NAME = "India"
    USER_NAME = "Christopher Tu"
    USER_GENDER = 'f'

    # country selector
    COUNTRY_SELECT = (AppiumBy.ID, "com.androidsample.generalstore:id/spinnerCountry")
    COUNTRY_SELECT_SCROLL = (AppiumBy.ANDROID_UIAUTOMATOR,
                             f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{COUNTRY_NAME}"))')
    COUNTRY_SELECT_TEXTVIEW = (AppiumBy.XPATH, f"//android.widget.TextView[@text='{COUNTRY_NAME}']")

    # username entry
    USER_ENTRY = (AppiumBy.ID, "com.androidsample.generalstore:id/nameField")

    # gender entry
    GENDER_ENTRY_F = (AppiumBy.ID, "com.androidsample.generalstore:id/radioFemale")
    GENDER_ENTRY_M = (AppiumBy.ID, "com.androidsample.generalstore:id/radioMale")

    # shop button
    SHOP_BUTTON = (AppiumBy.ID, "com.androidsample.generalstore:id/btnLetsShop")


class ProductPageLocators(object):
    # title bar
    PRODUCT_TITLE_BAR = (AppiumBy.XPATH, "//android.widget.TextView[@text='Products']")

    # item names to search for the store
    ITEMS = ["PG 3", "Nike SFB Jungle"]

    # cart button
    CART_BUTTON = (AppiumBy.ID, "com.androidsample.generalstore:id/appbar_btn_cart")

    # title bar
    TITLE_BAR = (AppiumBy.ID, "com.androidsample.generalstore:id/toolbar_title")


class CartPageLocators(object):
    # title bar
    TITLE_BAR = (AppiumBy.ID, "com.androidsample.generalstore:id/toolbar_title")

    # total purchase amount
    PURCHASE_AMOUNT = (AppiumBy.XPATH,
                       f"//android.widget.TextView[@text='Total Purchase Amount:  ']/following-sibling::android.widget.TextView[1]")

    # email checkbox
    EMAIL_CHECKBOX = (AppiumBy.XPATH,
                      "//android.widget.CheckBox[@text='Send me e-mails on discounts related to selected products in future']")

    # visit webpage button
    PROCEED_BUTTON = (AppiumBy.ID, "com.androidsample.generalstore:id/btnProceed")


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.WAIT_TIME = 50

    def get_element(self, locator_type, locator_string):
        """get element from page"""
        try:
            element = WebDriverWait(self.driver, self.WAIT_TIME).until(
                EC.presence_of_element_located((locator_type, locator_string))
            )
            return element
        except NoSuchElementException as e:
            print(f"Element with {locator_type} of {locator_string} not found", e)

    def get_text(self, locator_type, locator_string):
        """get text of page element"""
        element = self.get_element(locator_type, locator_string)
        return element.text

    def enter_text(self, locator_type, locator_string, text):
        """enter text into page element"""
        self.get_element(locator_type, locator_string).send_keys(text)

    def click(self, locator_type, locator_string):
        """click button on the page"""
        try:
            WebDriverWait(self.driver, self.WAIT_TIME).until(
                EC.element_to_be_clickable((locator_type, locator_string))
            ).click()
        except ElementClickInterceptedException as e:
            print(f"Element click intercepted for {locator_type} of {locator_string}", e)


class HomePage(BasePage):
    def select_country(self):
        self.click(*HomeScreenLocators.COUNTRY_SELECT)
        self.driver.find_element(*HomeScreenLocators.COUNTRY_SELECT_SCROLL)
        self.click(*HomeScreenLocators.COUNTRY_SELECT_TEXTVIEW)

    def enter_user_name(self):
        self.enter_text(*HomeScreenLocators.USER_ENTRY, HomeScreenLocators.USER_NAME)

    def select_gender(self, gender):
        if gender == 'F':
            self.click(*HomeScreenLocators.GENDER_ENTRY_F)
        elif gender == 'M':
            self.click(*HomeScreenLocators.GENDER_ENTRY_M)

    def click_shop_button(self):
        self.click(*HomeScreenLocators.SHOP_BUTTON)


class ProductPage(BasePage):
    def add_item(self, item_name):
        # item locator
        ITEM_LOCATOR = (AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{item_name}"))')

        self.driver.find_element(*ITEM_LOCATOR)

        # add to cart locators
        add_item_layout = self.get_element(AppiumBy.XPATH,
                                           f"//android.widget.TextView[@text='{item_name}']/following-sibling::android.widget.LinearLayout[2]")
        add_item_button = add_item_layout.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='ADD TO CART']")

        add_item_button.click()

        return self.get_element(AppiumBy.XPATH, f"//android.widget.TextView[@text='{item_name}']")

    def click_cart_button(self):
        self.click(*ProductPageLocators.CART_BUTTON)


class CartPage(BasePage):
    def get_item_price(self, item_name):
        # look for the price
        price_layout = self.driver.find_element(AppiumBy.XPATH,
                                                f"//android.widget.TextView[@text='{item_name}']/following-sibling::android.widget.LinearLayout[2]")
        price = price_layout.find_element(AppiumBy.XPATH, "//android.widget.TextView")

        return float(price.text[1:])

    def get_purchase_price(self):
        price_text = self.get_text(*CartPageLocators.PURCHASE_AMOUNT)
        return float(price_text[1:])

    def click_email_checkbox(self):
        self.click(*CartPageLocators.EMAIL_CHECKBOX)

    def click_proceed_button(self):
        self.click(*CartPageLocators.PROCEED_BUTTON)
