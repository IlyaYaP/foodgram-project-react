import allure

from src.base_validate import Response
from src.validation_schemes.subscribe_schemes import Subscribe, SubscribeErrors


class SubscribeValidate(Response):

    def subscribe_validate(self):
        with allure.step('Проверяем статус-код и валидность ответа:'):
            if self.response_status == 201:
                with allure.step('Статус-код 201, успешно подписались, проверяем валидность ответа.'):
                    Subscribe.parse_obj(self.response_json)
            elif self.response_status == 400:
                with allure.step('Статус-код 400, ошибка, проверяем валидность ответа.'):
                    SubscribeErrors.parse_obj(self.response_json)
                    print(f'status_code = {self.response_status}, respone = {self.response_json}')
            else:
                assert self.response_status != 400 or 201, 'Что то пошло не так.'
