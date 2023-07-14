from typing import Union

from pydantic import AnyUrl, BaseModel, Field, constr, validator

from src.errors import ErrorMessaages

from .ingredients_schemes import Ingredients
from .tags_schemes import Tags
from .user_schemes import Users


class RecipesResult(BaseModel):
    id: int
    tags: list[Tags]
    author: Users = Field(...)
    ingredients: list[Ingredients]
    is_favorited: bool = Field(...)
    is_in_shopping_cart: bool = Field(...)
    name: constr(max_length=150) = Field(...)
    image: AnyUrl
    text: str = Field(...)
    cooking_time: int = Field(...)


class RecipesPatch(BaseModel):
    id: int
    tags: list[Tags]
    author: Users = Field(...)
    ingredients: list[Ingredients]
    is_favorited: bool = Field(...)
    is_in_shopping_cart: bool = Field(...)
    name: constr(max_length=150) = Field(...)
    image: AnyUrl
    text: str = Field(...)
    cooking_time: int = Field(...)

    @validator('name')
    def name_validator(cls, value):
        if value != 'patch test recipe':
            raise ValueError(f'Ошибка валидации, {value}')
        return value

    @validator('text')
    def text_validator(cls, value):
        if value != 'path description test':
            raise ValueError(f'Ошибка валидации, {value}')
        return value


class Recipes(BaseModel):
    count: int
    next: Union[str, None]
    previous: Union[str, None]
    results: list[RecipesResult]


class RecipesValidationError(BaseModel):
    cooking_time: list = Field(...)

    @validator("cooking_time")
    def validate_cooking_time(cls, value):
        if value[0] not in ErrorMessaages.WRONG_VALIDATE_ERRORS:
            raise ValueError(f'Ошибка валидации, {value[0]}')


class RecipesNotLoggedError(BaseModel):
    detail: str = Field(...)


class RecipesFavorite(BaseModel):
    id: int
    name: constr(max_length=150) = Field(...)
    image: AnyUrl
    cooking_time: int = Field(...)


class RecipesFavoriteError(BaseModel):
    errors: list[str]
