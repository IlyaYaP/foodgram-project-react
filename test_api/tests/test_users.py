import allure
import pytest
import requests

from src.api_objects.users_object import UsersValidate
from src.base_validate import NoResponse, Response
from src.data import UsersData
from src.endpoints import UsersEndPoints
from src.validation_schemes.user_schemes import (InvalidChangingPassword,
                                                 InvalidUserRegistration,
                                                 UserList, Users,
                                                 UsersProfileError)


@pytest.mark.order(1)
@pytest.mark.users_tests(scope='class')
@allure.feature('Тесты работы с пользователем.')
class TestUsers():
    @pytest.mark.test_get_users_list
    @allure.story('Тест получения списка пользователей.')
    def test_get_users_list(self):
        r = requests.get(url=UsersEndPoints.LIST_USERS)
        response = Response(r)
        response.assert_status_code(200)
        response.validate(UserList)

    @pytest.mark.test_user_registration
    @allure.story('Тест регистрации пользователя.')
    def test_user_registration(self):
        r = requests.post(url=UsersEndPoints.USER_REGISTRATION,
                          data=UsersData.USER_REGISTRATION_DATA)
        response = UsersValidate(r)
        response.user_validate()

    @pytest.mark.test_negative_user_registration
    @allure.story('Негативный тест регистрации пользователя: \
                   указываем невалидные данные.')
    def test_negative_user_registration(self):
        r = requests.post(url=UsersEndPoints.USER_REGISTRATION,
                          data=UsersData.INVALID_USER_REGISTRATION_DATA)
        response = Response(r)
        response.assert_status_code(400)
        response.validate(InvalidUserRegistration)

    @pytest.mark.test_get_user_profile
    @allure.story('Тест получения информации профиля пользователей.')
    def test_get_user_profile(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.get(url=UsersEndPoints.USER_PROFILE, headers=headers)
        response = UsersValidate(r)
        response.assert_status_code(200)
        response.validate(Users)

    @pytest.mark.test_nagative_get_user_profile_object_not_found
    @allure.story('Тест получения информации о несуществующем пользователе.')
    def test_nagative_get_user_profile_object_not_found(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.get(url=UsersEndPoints.INVALIDE_USER_PROFILE,
                         headers=headers)
        response = UsersValidate(r)
        response.assert_status_code(404)
        response.validate(UsersProfileError)

    @pytest.mark.test_negative_get_user_profile_not_logged
    @allure.story('Тест получения информации о пользователе, без авторизации.')
    def test_negative_get_user_profile_not_logged(self):
        r = requests.get(url=UsersEndPoints.USER_PROFILE)
        response = UsersValidate(r)
        response.assert_status_code(401)
        response.validate(UsersProfileError)

    @pytest.mark.test_get_current_user
    @allure.story('Тест получения информации о текущем пользователе.')
    def test_get_current_user(self):
        r = requests.post(url=UsersEndPoints.USER_TOKEN,
                          data=UsersData.LOGIN_USER_TOKEN_DATA)
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.get(url=UsersEndPoints.CURRENT_USER, headers=headers)
        response = UsersValidate(r)
        response.assert_status_code(200)
        response.validate(Users)

    @pytest.mark.test_negative_get_current_user_not_logged
    @allure.story('Тест получения информации о текущем пользователе, без авторизации.')
    def test_negative_get_current_user(self):
        r = requests.get(url=UsersEndPoints.CURRENT_USER)
        response = UsersValidate(r)
        response.assert_status_code(401)
        response.validate(UsersProfileError)

    @pytest.mark.test_changing_password
    @allure.story('Тест изменения пароля.')
    def test_changing_password(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.post(url=UsersEndPoints.CHANGING_PASSWORD,
                          data=UsersData.CHANGING_PASSWORD_DATA,
                          headers=headers)
        if r.status_code == 204:
            requests.post(url=UsersEndPoints.CHANGING_PASSWORD,
                          data=UsersData.RETURN_CHANGING_PASSWORD_DATA,
                          headers=headers)
        else:
            assert f'Статус код = {r.status_code}'

    @pytest.mark.test_changing_password_user_not_logged
    @allure.story('Тест изменения пароля, без авторизации.')
    def test_negative_changing_password_user_not_logged(self):
        r = requests.post(url=UsersEndPoints.CHANGING_PASSWORD,
                          data=UsersData.CHANGING_PASSWORD_DATA)
        response = UsersValidate(r)
        response.assert_status_code(401)
        response.validate(UsersProfileError)

    @pytest.mark.test_changing_password_validation_error
    @allure.story('Тест изменения пароля, с некорректными данными.')
    def test_negative_changing_password_validation_error(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.post(url=UsersEndPoints.CHANGING_PASSWORD,
                          data=UsersData.INVALIDE_CHANGING_PASSWORD_DATA,
                          headers=headers)
        response = UsersValidate(r)
        response.assert_status_code(400)
        response.validate(InvalidChangingPassword)

    @pytest.mark.test_delete_token
    @allure.story('Тест удаления токена.')
    def test_delete_token(self):
        headers = Response.user_auth_token(
                  data=UsersData.LOGIN_USER_TOKEN_DATA)
        r = requests.post(url=UsersEndPoints.DELETE_TOKEN,
                          headers=headers)
        response = NoResponse(r)
        response.assert_status_code(204)

    @pytest.mark.test_delete_token_user_not_logged
    @allure.story('Тест удаления токена, без авторизации.')
    def test_negative_delete_token_user_not_logged(self):
        r = requests.post(url=UsersEndPoints.DELETE_TOKEN)
        response = NoResponse(r)
        response.assert_status_code(401)
