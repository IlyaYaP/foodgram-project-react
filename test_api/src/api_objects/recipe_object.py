import allure
import requests

from src.base_validate import Response
from src.validation_schemes.recipes_schemes import RecipesResult


class RecipeValidate(Response):

    def recipe_validate(self):
        with allure.step('Проверяем статус-код и валидность ответа:'):
            if self.response_status == 200:
                with allure.step('Статус-код 200, получили рецепт, проверяем валидность ответа.'):
                    RecipesResult.parse_obj(self.response_json)
                    print(f'status_code = {self.response_status}, respone = {self.response_json}')
            else:
                assert self.response_status == 404, 'Проверьте, что в url указан id существующего рецепта'

    def recipe_id(url):
        recipes_list = requests.get(url=url)
        recipe_id = recipes_list.json()['results'][0]['id']
        return recipe_id
