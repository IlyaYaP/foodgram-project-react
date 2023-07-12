from pydantic import AnyUrl, BaseModel, Field, constr


class ShoppingCart(BaseModel):
    id: int
    name: constr(max_length=150) = Field(...)
    image: AnyUrl
    cooking_time: int = Field(...)


class ShoppingCartError(BaseModel):
    errors: list[str]
