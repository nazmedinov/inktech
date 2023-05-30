import time
import allure

from selenium.webdriver.support.ui import WebDriverWait
from qa_core.qa_core_settings import QaCoreSettings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains


class SeleniumWrapper:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    @allure.step("Открытие страницы в браузере")
    def open(self):
        self.browser.get(self.url)

    @allure.step("Установка размера страницы в браузере")
    def set_viewport(self, width):
        self.browser.set_window_size(int(width), 1000)

    @allure.step("Проскролить к элементу")
    def in_scroll_to_element(self, how, what):
        time.sleep(3)
        element = self.browser.find_element(how, what)
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step("Ожидание пока элемент будет видимым на странице")
    def wait_for_visibility(self, how, what, timeout=QaCoreSettings.TIME_OUT, step=QaCoreSettings.STEP):
        WebDriverWait(self.browser, timeout, step).until(ec.visibility_of_element_located((how, what)))

    @allure.step("Ожидание пока элемент не будет видимым на странице")
    def wait_for_invisibility(self, how, what, timeout=QaCoreSettings.TIME_OUT, step=QaCoreSettings.STEP):
        WebDriverWait(self.browser, timeout, step).until_not(ec.visibility_of_element_located((how, what)))

    @allure.step("Видимость элемента на странице")
    def is_element_visible(self, how, what, timeout=QaCoreSettings.TIME_OUT, step=QaCoreSettings.STEP):
        try:
            WebDriverWait(self.browser, timeout, step).until(ec.visibility_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    @allure.step("Невидимость элемента на странице")
    def is_not_element_visible(self, how, what, timeout=5):
        try:
            WebDriverWait(self.browser, timeout).until(ec.visibility_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    @allure.step("Ожидание видимости элемента и клик на него")
    def wait_and_click(self, how, what, timeout=QaCoreSettings.TIME_OUT, step=QaCoreSettings.STEP):
        WebDriverWait(self.browser, timeout, step).until(ec.visibility_of_element_located((how, what)))
        self.browser.find_element(how, what).click()

    @staticmethod
    @allure.step("Переключение на вторую вкладку браузера")
    def switch_to_next_window(browser):
        browser.switch_to.window(browser.window_handles[1])

    @staticmethod
    @allure.step("Переключение на первую вкладку браузера")
    def switch_to_previous_window(browser):
        browser.switch_to.window(browser.window_handles[0])

    @allure.step("Наводим курсор на элемент")
    def move_to_element(self, how, what):
        self.wait_for_visibility(how, what)
        element = self.browser.find_element(how, what)
        ActionChains(self.browser).move_to_element(element).perform()

    @allure.step("Исчезновение элемента")
    def is_disappeared(self, how, what, timeout=5, step=QaCoreSettings.STEP):
        try:
            WebDriverWait(self.browser, timeout, step).until_not(ec.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    @allure.step("Появление элемента на странице")
    def is_appeared(self, how, what, timeout=5, step=QaCoreSettings.STEP):
        try:
            WebDriverWait(self.browser, timeout, step).until_not(ec.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    @allure.step("Наличие элемента на странице в DOM страницы")
    def is_element_present(self, how, what, timeout=QaCoreSettings.TIME_OUT, step=QaCoreSettings.STEP):
        try:
            WebDriverWait(self.browser, timeout, step).until(ec.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    @allure.step("Отсутствие элемента на странице в DOM страницы")
    def is_not_element_present(self, how, what, timeout=5):
        try:
            WebDriverWait(self.browser, timeout).until(ec.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    @allure.step("Находим элемент и вводим значение")
    def set_value(self, how, what, value):
        self.is_element_visible(how, what)
        self.browser.find_element(how, what).click()
        self.browser.find_element(how, what).send_keys(value)

    @allure.step("Открываем новую вкладку браузера")
    def open_new_tab(self):
        self.browser.execute_script("""window.open("http://bings.com","_blank");""")
        self.browser.switch_to.window(self.browser.window_handles[1])

    @allure.step("Дважды кликаем на элемент")
    def double_click(self, how, what):
        self.wait_for_visibility(how, what)
        element = self.browser.find_element(how, what)
        action = ActionChains(self.browser)
        # move to element operation
        action.double_click(element).perform()

    @allure.step("Появление алерта на странице")
    def is_alert_present(self, timeout=15, step=QaCoreSettings.STEP):
        try:
            WebDriverWait(self.browser, timeout, step).until(ec.alert_is_present())
        except TimeoutException:
            return False
        return True
