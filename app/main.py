from fastapi import FastAPI
from app.routers.home import home_router
from app.routers.auth_user import auth_router
from app.routers.root import root_router
from app.routers.user import user_router
from app.routers.admin import admin_router
from app.routers.category import category_router
from app.routers.product import product_router

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
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(product_router)