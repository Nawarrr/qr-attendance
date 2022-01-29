
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

# TO DO 

# AUTHENTICATION CURRENTLY UNDER WORK 

# app.include_router(auth.router)


# SECRET_KEY = os.environ.get('SECRET_KEY') or None
# if SECRET_KEY is None:
#     raise 'Missing SECRET_KEY'
# app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


