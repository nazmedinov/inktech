import allure

from pages.base_page import BasePage
from tests.base_test import BaseTest
from selenium.webdriver.common.by import By
from pages.base_page import BasePageLocators
# from tests.api_tests.http_manager import HttpManager, JSON_Fixtures, Roots


class ClientPageLocators(BasePageLocators):
    # xpath кнопки about us
    BUTTON_ABOUT_US = (By.XPATH, "//div[contains(@class, 'menu')]//a[@href='/about'][@class]")
    # xpath заголовка страницы about us
    TITLE_PAGE_ABOUT_US = (By.XPATH, "//div[@class='tn-atom'][text()='Inktech']")
    # Блок с преимуществами компании
    BLOCK_ADVANTAGES = (By.XPATH, "//div[@class='t396__filter'][@data-artboard-recid='568093052']")


class ClientPage(BasePage):
    def __init__(self, browser):
        super(ClientPage, self).__init__(browser, BaseTest.CLIENT_URL)
