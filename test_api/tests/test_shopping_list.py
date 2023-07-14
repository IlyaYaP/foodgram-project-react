from pathlib import Path

import allure
import pytest
import requests

from src.api_objects.recipe_object import RecipeValidate
from src.api_objects.shopping_cart_object import ShoppingCartValidate
from src.base_validate import NoResponse, Response
from src.data import UsersData
from src.endpoints import RecipesEndPoints, ShoppingCartEndPoints
from src.validation_schemes.errors_schemes import Error401


@pytest.mark.order(5)
@pytest.mark.shopping_cart_tests(scope='class')
@allure.feature('Тесты добавления рецептов в список покупок.')
class TestShoppingCart():
    @pytest.mark.test_add_shopping_cart
    @allure.story('Тест добавления рецептов в список покупок.')
    def test_add_shopping_cart(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        url_shopping_cart = f'http://localhost/api/recipes/{recipe_id}/shopping_cart/'
        r = requests.post(url=url_shopping_cart, headers=headers)
        response = ShoppingCartValidate(r)
        response.shopping_cart_validate()

    @pytest.mark.test_download_shopping_cart
    @allure.story('Тест скачивания списка покупок.')
    def test_download_shopping_cart(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.get(url=ShoppingCartEndPoints.DOWNLOAD_SHOPPING_CART,
                         headers=headers)
        with allure.step('Скачем списко покупок и проверим, что он появился в корне проекта.'):
            if r.status_code == 200:
                filename = Path('shopping_cart.pdf')
                filename.write_bytes(r.content)
            else:
                assert f'Статус код = {r.status_code}'

    @pytest.mark.test_negative_download_shopping_cart_not_logged
    @allure.story('Тест скачивания списка покупок, без авторизации')
    def test_negative_download_shopping_cart_not_logged(self):
        r = requests.get(url=ShoppingCartEndPoints.DOWNLOAD_SHOPPING_CART)
        response = Response(r)
        response.assert_status_code(401)
        response.validate(Error401)

    @pytest.mark.test_delete_shopping_cart
    @allure.story('Тест удаления рецептов из списка покупок.')
    def test_delete_shopping_cart(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        url_shopping_cart = f'http://localhost/api/recipes/{recipe_id}/shopping_cart/'
        r = requests.delete(url=url_shopping_cart, headers=headers)
        response = NoResponse(r)
        response.assert_status_code(204)

    @pytest.mark.test_negative_delete_shopping_cart_not_logged
    @allure.story('Тест скачивания списка покупок, без авторизации')
    def test_negative_delete_shopping_cart_not_logged(self):
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        url_shopping_cart = f'http://localhost/api/recipes/{recipe_id}/shopping_cart/'
        r = requests.delete(url=url_shopping_cart)
        response = NoResponse(r)
        response.assert_status_code(401)
