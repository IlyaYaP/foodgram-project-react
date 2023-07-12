from pydantic import BaseModel, Field, constr
from pydantic.color import Color


class Tags(BaseModel):
    id: int
    name: constr(max_length=200)
    color: Color
    slug: constr(max_length=200) = Field(regex='^[-a-zA-Z0-9_]+$')


class TagsError(BaseModel):
    detail: str
