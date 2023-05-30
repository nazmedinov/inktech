from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from qa_core.qa_core_settings import QaCoreSettings
from tests.base_test import BaseTest


def create(browser_name, width, language):
    print(f"\nstart {browser_name} browser for test..")
    if browser_name == "chrome":
        # Список опций можно посмотреть тут: https://peter.sh/experiments/chromium-command-line-switches/
        # Список настраиваемых возможностей: https://www.lambdatest.com/support/docs/selenium-automation-capabilities/
        options = Options()
        # Настроить версию браузера:
        # options.set_capability("browserVersion", QaCoreSettings.CHROME_BROWSER_VERSION)
        # Настроить язык браузера:
        options.add_experimental_option("prefs", {"intl.accept_languages": language})
        # Отключить в браузере политику разрешенных доменов:
        options.add_argument("--disable-web-security")
        # Отключить механизм безопасности браузера:
        options.add_argument("--no-sandbox")
        # Настроить работу браузера в фоновом режиме без окон:
        options.add_argument("--headless")
        # Игнорировать ошибки SSL сертификатов:
        options.add_argument("--ignore-certificate-errors")
        # Разрешение загрузки небезопасного контента:
        options.add_argument("--allow-running-insecure-content")
        # Установить user agent для браузера:
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/60.0.3112.50 Safari/537.36"
        )
        # Установить максимальный размер экрана:
        options.add_argument("--start-maximized")  # for max size window

        # Инициализация браузера:
        browser = webdriver.Remote(command_executor=BaseTest.MOON_URL, options=options)
        # Настроить размер окна браузера:
        # browser.set_window_size(int(width), 1300)  # set window size
        return browser

    elif browser_name == "firefox":
        options = FirefoxOptions()
        # Настроить язык браузера:
        options.set_preference("intl.accept_languages", language)
        # Настроить версию браузера:
        options.set_capability("browserVersion", QaCoreSettings.FIREFOX_BROWSER_VERSION)

        # Инициализация браузера:
        browser = webdriver.Remote(command_executor=BaseTest.MOON_URL, options=options)
        # browser.maximize_window()
        browser.set_window_size(int(width), 1300)
        return browser

    else:
        print(f"Browser {browser_name} still is not implemented")
