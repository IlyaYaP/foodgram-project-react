from pydantic import BaseModel, Field


class Error401(BaseModel):
    detail: str = Field(...)


class Error400(BaseModel):
    errors: list[str]
