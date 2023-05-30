import pytest
import allure

from tests.api_tests.http_manager import HttpManager, Roots
from tests.base_test import BaseTest
from tests.errors_messages import ErrorsMessages


@allure.epic("Пользовательские руты: feed")
@allure.feature("GET")
@pytest.mark.api
class TestUserGetTagsApi:
    @allure.story("Получение списка новостей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_get_tags(self):
        result = HttpManager.get(BaseTest.API_CLIENT_URL + Roots.root_user_feeds)
        with allure.step("Проверяем код ответа"):
            assert result.status_code == 200, ErrorsMessages.WRONG_STATUS_CODE
