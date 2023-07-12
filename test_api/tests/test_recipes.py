import allure
import pytest
import requests

from src.api_objects.recipe_object import RecipeValidate
from src.base_validate import Response
from src.data import RecipeData, UsersData
from src.endpoints import RecipesEndPoints
from src.validation_schemes.errors_schemes import Error401
from src.validation_schemes.recipes_schemes import (Recipes, RecipesPatch,
                                                    RecipesResult,
                                                    RecipesValidationError)


@pytest.mark.order(2)
@pytest.mark.recipe_creation_tests(scope='class')
@allure.feature('Тесты создания рецептов.')
class TestRecipeCreation():

    @pytest.mark.test_create_recipe
    @allure.story('Тест создания рецепта.')
    def test_create_recipe(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.post(url=RecipesEndPoints.RECIPES_LIST,
                          json=RecipeData.RECIPE_CREATE_DATA,
                          headers=headers)
        response = Response(r)
        response.assert_status_code(201)
        response.validate(RecipesResult)

    @pytest.mark.test_negative_create_recipe_validation_error
    @allure.story('Тест создания рецепта с невалидными данными.')
    def test_negative_create_recipe_validation_error(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.post(url=RecipesEndPoints.RECIPES_LIST,
                          json=RecipeData.INVALID_RECIPE_CREATE_DATA,
                          headers=headers)
        response = Response(r)
        response.assert_status_code(400)
        response.validate(RecipesValidationError)

    @pytest.mark.test_negative_create_recipe_user_not_logged
    @allure.story('Тест создания рецепта, без авторизации.')
    def test_negative_create_recipe_user_not_logged(self):
        r = requests.post(url=RecipesEndPoints.RECIPES_LIST,
                          json=RecipeData.INVALID_RECIPE_CREATE_DATA)
        response = Response(r)
        response.assert_status_code(401)
        response.validate(Error401)

    @pytest.mark.test_get_recipe
    @allure.story('Тест получения рецепта.')
    def test_get_recipe(self):
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        r = requests.get(url=f'http://localhost/api/recipes/{recipe_id}/')
        response = Response(r)
        response.assert_status_code(200)
        response.validate(RecipesResult)

    @pytest.mark.test_get_recipes_list
    @allure.story('Тест получения списка рецептов.')
    def test_recipes_list(self):
        r = requests.get(url=RecipesEndPoints.RECIPES_LIST)
        response = Response(r)
        response.assert_status_code(200)
        response.validate(Recipes)

    @pytest.mark.test_patch_recipe
    @allure.story('Тест изменения рецепта.')
    def test_patch_recipe(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        r = requests.patch(url=f'http://localhost/api/recipes/{recipe_id}/',
                           json=RecipeData.RECIPE_PATCH_DATA,
                           headers=headers)
        response = Response(r)
        response.assert_status_code(200)
        response.validate(RecipesPatch)

    @pytest.mark.test_negative_patch_recipe_validation_error
    @allure.story('Тест изменения рецепта c невалидными данными.')
    def test_negative_patch_recipe_validation_error(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        r = requests.patch(url=f'http://localhost/api/recipes/{recipe_id}/',
                           json=RecipeData.INVALID_RECIPE_PATCH_DATA,
                           headers=headers)
        response = Response(r)
        response.assert_status_code(400)
        response.validate(RecipesValidationError)

    @pytest.mark.test_patch_recipe_user_not_logged
    @allure.story('Тест изменения рецепта, без авторизации.')
    def test_patch_recipe_user_not_logged(self):
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        r = requests.patch(url=f'http://localhost/api/recipes/{recipe_id}/',
                           json=RecipeData.RECIPE_PATCH_DATA)
        response = Response(r)
        response.assert_status_code(401)
        response.validate(Error401)

    @pytest.mark.test_delete_recipe
    @allure.story('Тест удаления рецепта.')
    def test_delete_recipe(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        recipe_id = RecipeValidate.recipe_id(url=RecipesEndPoints.RECIPES_LIST)
        r = requests.delete(url=f'http://localhost/api/recipes/{recipe_id}/',
                            headers=headers)
        if r.status_code == 204:
            self.test_create_recipe()
        else:
            assert f'{r.status_code}'
