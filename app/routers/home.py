from fastapi import APIRouter
from app.schemas.message_schema import MessageResponseSchema

home_router = APIRouter(prefix="/home")


@home_router.get(
    "/",
    status_code=200,
    response_model=MessageResponseSchema,
    summary="Головна сторінка API",
    description="""
    Повертає привітальне повідомлення для користувача.
    Використовується для перевірки доступності API після запуску.
    """
)
def home_page():
    return {"message": "Вітаємо на головній сторінці!"}
