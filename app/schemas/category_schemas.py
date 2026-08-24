from app.schemas.base_schema import BaseSchema


class CategoryCreateSchema(BaseSchema):
    name: str
    description: str | None = None


class CategoryResponseSchema(CategoryCreateSchema):
    id: int
    name: str
    description: str | None = None


class CategoryUpdateSchema(BaseSchema):
    name: str | None = None
    description: str | None = None
