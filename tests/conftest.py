import pytest
import allure

from qa_core.driver_provider import create
from pages.client_main_page import ClientPage
from tests.base_test import BaseTest


# Функция добавления пользовательских опций в командной строке
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="Choose browser: chrome or firefox")
    parser.addoption("--width", action="store", default="1280", help="Choose width")
    parser.addoption("--language", action="store", default="en", help="Choose language")


# Фикстура для передачи параметра browser_name в тесты
@pytest.fixture(scope="session")
def browser_name(request):  # request - это встроенная фикстура
    browser_name = request.config.getoption("--browser_name")
    yield browser_name


# Фикстура для передачи параметра width в тесты
@pytest.fixture(scope="session")
def width(request):  # request - это встроенная фикстура
    width = request.config.getoption("--width")
    yield width


# Фикстура для передачи параметра language в тесты
@pytest.fixture(scope="session")
def language(request):  # request - это встроенная фикстура
    language = request.config.getoption("--language")
    yield language


# Инициализация и настройка браузеров Chrome и Firefox
@pytest.fixture(scope="function")
def browser(browser_name, width, language, request):
    with allure.step("Инициализация и настройка браузера"):
        browser = create(browser_name, width, language)
        browser.implicitly_wait(1)  # Настройка времени неявного ожидания в браузере
    yield browser  # Код после yield выполнится даже если тест упадет с ошибкой
    browser.quit()
    print("\nquit browser..")


#  Инициализация и открытие главной страницы
@pytest.fixture(scope="function")
def client_page(browser):
    with allure.step("Открытие главной страницы сайта: клиенсткая часть"):
        client_page = ClientPage(browser)
        client_page.open()
        yield client_page
