from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger
# from sqlalchemy import select, text
from sqlalchemy.exc import NoResultFound
# from database.database import session_manager
# from database.models.user import User
from endpoints.user import router as router_user
from endpoints.post import router as router_post
from core.exceptions import setup_exception_handlers

app = FastAPI(
     title="My Day API",
     description="API for microblogging",
     version="0.1.0"
)



     
app.include_router(router_user)
app.include_router(router_post)
setup_exception_handlers(app)

# @app.get("/")
# def hello_world():
#      with session_manager() as session:
#           result = session.execute(text('SELECT 1'))
#           print(result)

#           query = select(User)
#           rsp = session.execute(query)
#           print(rsp)

#      return {"hello": "World"}