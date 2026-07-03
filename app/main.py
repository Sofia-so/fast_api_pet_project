from fastapi import FastAPI
from app.routers.home import home_router
from app.routers.auth_user import auth_router
from app.routers.root import root_router
from app.routers.user import user_router

app = FastAPI(
    title="API",
    version="v1",
    openapi_url="/api/openapi.json",
    docs_url="/docs"
)

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(root_router)
app.include_router(user_router)