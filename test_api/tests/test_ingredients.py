import allure
import pytest
import requests

from src.base_validate import Response
from src.endpoints import IngredientsEndPoints
from src.validation_schemes.ingredients_schemes import Ingredients


@pytest.mark.order(6)
@pytest.mark.ingredients_tests(scope='class')
@allure.feature('Тесты получения списка рецептов.')
class TestIngredients():
    @pytest.mark.test_ingredients_list
    @allure.story('Тест получения списка рецептов.')
    def test_ingredients_list(self):
        r = requests.get(url=IngredientsEndPoints.INGREDIENTS_LIST)
        response = Response(r)
        response.assert_status_code(200)
        response.validate(Ingredients)

    @pytest.mark.test_get_ingredient
    @allure.story('Тест получения определенного ингредиента.')
    def test_get_ingredient(self):
        r = requests.get(url='http://localhost/api/ingredients/123/')
        response = Response(r)
        response.assert_status_code(200)
        response.validate(Ingredients)
