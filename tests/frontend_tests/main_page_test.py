import pytest
import allure

from qa_core.screenshooter import ScreenShooter
from pages.client_main_page import ClientPageLocators
from tests.base_test import BaseTest
from tests.errors_messages import ErrorsMessages as Em


@allure.epic("Главная страница")
@pytest.mark.usefixtures("client_page")
class TestClientPage(BaseTest):
    @allure.feature("Хедер сайта")
    @allure.story("Отображение хедера главной страницы")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("screen_name", ["HEADER_MAIN_PAGE"])
    def test_user_can_see_header(self, browser, client_page, screen_name, width, language, browser_name):
        sc = ScreenShooter()
        element = ClientPageLocators.HEADER
        client_page.scroll_to_element(*element)
        with allure.step("Сравнение текущего скриншота Хедера с базовым изображением в хранилище"):
            sc.check_s3_images(browser, screen_name, width, language, browser_name, element)

    @allure.feature("Хедер сайта")
    @allure.story("Кнопка about us")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("screen_name", ["BUTTON_ABOUT_US"])
    def test_user_can_see_header(self, browser, client_page, screen_name, width, language, browser_name):
        sc = ScreenShooter()
        client_page.wait_and_click(*ClientPageLocators.BUTTON_ABOUT_US)
        assert "about" in browser.current_url, Em.WRONG_URL
        element = ClientPageLocators.TITLE_PAGE_ABOUT_US
        with allure.step("Сравнение текущего скриншота Хедера с базовым изображением в хранилище"):
            sc.check_s3_images(browser, screen_name, width, language, browser_name, element)
