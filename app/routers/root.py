from fastapi import APIRouter
from fastapi.responses import RedirectResponse

root_router = APIRouter()


@root_router.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")