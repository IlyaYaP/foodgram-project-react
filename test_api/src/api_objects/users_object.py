import allure
import requests

from src.base_validate import Response
from src.errors import ErrorMessaages
from src.validation_schemes.user_schemes import (InvalidUserRegistration,
                                                 UserRegistration)


class UsersValidate(Response):

    def user_validate(self):
        with allure.step('Проверяем статус-код и валидность ответа:'):
            if self.response_status == 200:
                with allure.step('Статус-код 200, пользователь успешно зарегистрирован, проверяем валидность ответа.'):
                    UserRegistration.parse_obj(self.response_json)
                    print(f'status_code = {self.response_status}, respone = {self.response_json}')
            elif self.response_status == 400:
                with allure.step('Статус-код 400, пользователь с такими данными уже существует, проверяем валидность ответа.'):
                    InvalidUserRegistration.parse_obj(self.response_json)
                    print(f'status_code = {self.response_status}, respone = {self.response_json}')
            else:
                assert self.response_status != 400 or 200, 'Что то пошло не так.'

    def user_assert_status_code(self, statuse_code):
        '''Функция проверки статус код.'''
        with allure.step(f'Проверяем статус-код ответа. Ожидем = {statuse_code}'):
            if isinstance(statuse_code, list):
                assert self.response_status in statuse_code, f'{ErrorMessaages.WRONG_STATUS_CODE}, status code = {self.response_status}, {self.response_json}'
            else:
                assert self.response_status == statuse_code, f'{ErrorMessaages.WRONG_STATUS_CODE}, status code = {self.response_status}, {self.response_json}'

    def user_id(url):
        user_list = requests.get(url=url)
        user_id = user_list.json()['results'][0]['id']
        return user_id
