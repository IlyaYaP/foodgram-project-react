import allure
import requests

from src.endpoints import UsersEndPoints
from src.errors import ErrorMessaages


class Response():
    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.response_status = response.status_code

    def validate(self, schema):
        '''Функция проверки валидности ответа.'''
        with allure.step('Проверяем дынные ответа на валидность'):
            if isinstance(self.response_json, list):
                for item in self.response_json:
                    schema.parse_obj(item)
            else:
                schema.parse_obj(self.response_json)

    def assert_status_code(self, statuse_code):
        '''Функция проверки статус код.'''
        with allure.step(f'Проверяем статус-код ответа. Ожидем = {statuse_code}'):
            if isinstance(statuse_code, list):
                assert self.response_status in statuse_code, f'{ErrorMessaages.WRONG_STATUS_CODE}, status code = {self.response_status}, {self.response_json}'
            else:
                assert self.response_status == statuse_code, f'{ErrorMessaages.WRONG_STATUS_CODE}, status code = {self.response_status}, {self.response_json}'

    def user_auth_token(data):
        with allure.step('Получаем токен.'):

            r = requests.post(url=UsersEndPoints.USER_TOKEN, data=data)
            user_token = r.json()["auth_token"]
            headers = {'Authorization': f'Token {user_token}'}
            return headers


class NoResponse():
    def __init__(self, response):
        self.response = response
        self.response_status = response.status_code

    def assert_status_code(self, statuse_code):
        '''Функция проверки статус код.'''
        with allure.step(f'Проверяем статус-код ответа. Ожидем = {statuse_code}'):
            if isinstance(statuse_code, list):
                assert self.response_status in statuse_code, f'{ErrorMessaages.WRONG_STATUS_CODE}, status code = {self.response_status}'
            else:
                assert self.response_status == statuse_code, f'{ErrorMessaages.WRONG_STATUS_CODE}, status code = {self.response_status}'
