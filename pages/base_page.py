from selenium.webdriver.common.by import By
from qa_core.selenium_wrapper import SeleniumWrapper


class BasePageLocators(object):
    # xpath хедера сайта
    HEADER = (By.XPATH, "//div[contains(@class, 'js__menu')]")


class BasePage(SeleniumWrapper):
    pass
