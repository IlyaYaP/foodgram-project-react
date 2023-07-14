from pydantic import BaseModel, Field, constr


class Ingredients(BaseModel):
    id: int
    name: constr(max_length=200) = Field(...)
    measurement_unit: constr(max_length=200) = Field(...)
