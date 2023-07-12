import allure
import pytest
import requests

from src.base_validate import Response

from src.endpoints import TagsEndPoints
from src.validation_schemes.tags_schemes import Tags, TagsError


@pytest.mark.order(7)
@pytest.mark.tags_tests(scope='class')
@allure.feature('Тесты получения списка тегов.')
class TestTags():
    @pytest.mark.test_tags_list
    @allure.story('Тест получения списка тегов.')
    def test_tags_list(self):
        r = requests.get(url=TagsEndPoints.LIST_TAGS)
        response = Response(r)
        response.assert_status_code(200)
        response.validate(Tags)

    @pytest.mark.test_negative_not_found
    @allure.story('Тест получения несуществующего тега.')
    def test_negative_tags_not_found(self):
        r = requests.get(url=TagsEndPoints.TAGS_NOT_FOUND)
        response = Response(r)
        response.assert_status_code(404)
        response.validate(TagsError)
