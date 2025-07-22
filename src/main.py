from fastapi import FastAPI

from endpoints.user import router as router_user
from endpoints.post import router as router_post
from core.exceptions import setup_exception_handlers

app = FastAPI(title="My Day API", description="API for microblogging", version="0.1.0")

app.include_router(router_user)
app.include_router(router_post)
setup_exception_handlers(app)
