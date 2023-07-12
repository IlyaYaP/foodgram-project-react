class UsersData():
    USER_REGISTRATION_DATA = {
                                "email": "vpupki@nyandex.ru",
                                "username": "vasya.pupkin",
                                "first_name": "Вася",
                                "last_name": "Пупкин",
                                "password": "Qwerty12asd3"
                                }

    INVALID_USER_REGISTRATION_DATA = {
                                "email": "vpupkiyandex.ru",
                                "username": "vasya. pupkin",
                                "first_name": "Вася!)(*(№;))",
                                "last_name": "Пупкин",
                                "password": "Qwerty12asd3"
                                }

    LOGIN_USER_TOKEN_DATA = {

                            "password": "Qwerty12asd3",
                            "email": "vpupki@nyandex.ru"

                            }
    INVALID_LOGIN_USER_TOKEN_DATA = {

                            "password": "Qwerty2asd3",
                            "email": "vpupki@nyandex.ru"

                            }
    
    CHANGING_PASSWORD_DATA = {

                        "new_password": "Awerty2asd3",
                        "current_password": "Qwerty12asd3"

                        }
    
    RETURN_CHANGING_PASSWORD_DATA = {

                        "new_password": "Qwerty12asd3",
                        "current_password": "Awerty2asd3"

                        }

    INVALIDE_CHANGING_PASSWORD_DATA = {

                        "new_password": "Awerty2asd3"

                        }


class RecipeData():
    RECIPE_CREATE_DATA = {
                            "ingredients": [
                                {
                                    "id": 1123,
                                    "amount": 10
                                }
                            ],
                            "tags": [
                                1,
                                2
                            ],
                            "image": "data:image/png;base64, \
                                        iVBORw0KGgoAAAANSUhEUgAAAAEAAA\
                                        ABAgMAAABieywaAAAACVBMVEUAAAD\
                                        ///9fX1/S0ecCAAAACXBIWXMAAA\
                                        7EAAAOxAGVKw4bAAAACklEQVQI\
                                        mWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                            "name": "test recipe",
                            "text": "description test",
                            "cooking_time": 1
                        }


    INVALID_RECIPE_CREATE_DATA = {
                            "ingredients": [
                                {
                                    "id": 1123,
                                    "amount": 10
                                }
                            ],
                            "tags": [
                                1,
                                2
                            ],
                            "image": "data:image/png;base64, \
                                        iVBORw0KGgoAAAANSUhEUgAAAAEAAA\
                                        ABAgMAAABieywaAAAACVBMVEUAAAD\
                                        ///9fX1/S0ecCAAAACXBIWXMAAA\
                                        7EAAAOxAGVKw4bAAAACklEQVQI\
                                        mWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                            "name": "test recipe",
                            "text": "description test",
                            "cooking_time": "str"
                        }

    RECIPE_PATCH_DATA = {
                            "ingredients": [
                                {
                                    "id": 1123,
                                    "amount": 10
                                }
                            ],
                            "tags": [
                                1,
                                2
                            ],
                            "image": "data:image/png;base64, \
                                        iVBORw0KGgoAAAANSUhEUgAAAAEAAA\
                                        ABAgMAAABieywaAAAACVBMVEUAAAD\
                                        ///9fX1/S0ecCAAAACXBIWXMAAA\
                                        7EAAAOxAGVKw4bAAAACklEQVQI\
                                        mWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                            "name": "patch test recipe",
                            "text": "path description test",
                            "cooking_time": 1
                        }

    INVALID_RECIPE_PATCH_DATA = {
                            "ingredients": [
                                {
                                    "id": 1123,
                                    "amount": 10
                                }
                            ],
                            "tags": [
                                1,
                                2
                            ],
                            "image": "data:image/png;base64, \
                                        iVBORw0KGgoAAAANSUhEUgAAAAEAAA\
                                        ABAgMAAABieywaAAAACVBMVEUAAAD\
                                        ///9fX1/S0ecCAAAACXBIWXMAAA\
                                        7EAAAOxAGVKw4bAAAACklEQVQI\
                                        mWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                            "name": "patch test recipe",
                            "text": "path description test",
                            "cooking_time": "str"
                        }