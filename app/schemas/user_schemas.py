from pydantic import (
    EmailStr,
    model_validator
)
from app.schemas.base_schema import BaseSchema
from app.db.model_enum import UserRole


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
    role: UserRole


class UserUpdateSchema(BaseSchema):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: EmailStr | None = None


class UserChangePasswordSchema(BaseSchema):
    current_password: str
    new_password: str
    confirm_new_password: str

    @model_validator(mode="after")
    def confirm_password(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("Паролі не співпадають")
        return self
