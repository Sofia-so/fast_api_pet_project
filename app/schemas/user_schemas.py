from pydantic import (
    EmailStr,
    model_validator
)
from app.schemas.base_schema import BaseSchema


class UserBaseSchema(BaseSchema):
    first_name: str
    last_name: str
    username: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Паролі не співпадають")
        return self


class UserResponseSchema(UserBaseSchema):
    id: int
