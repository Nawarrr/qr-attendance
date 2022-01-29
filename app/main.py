
from fastapi import FastAPI 
from routers import classes , student ,auth
import models 
from database import engine 
import os
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
load_dotenv()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(classes.router)

app.include_router(student.router)


