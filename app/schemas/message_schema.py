from pydantic import BaseModel


class MessageResponseSchema(BaseModel):
    message: str
    docs_url: str | None = None
