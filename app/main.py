from fastapi import FastAPI , Request, Form , Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import qrcode
#import forms 
from datetime import datetime

import uvicorn 
#import pandas as pd 
import schemas ,models
from database import engine , SessionLocal
from sqlalchemy.orm.session import Session
import os
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse ,StreamingResponse
from authlib.integrations.starlette_client import OAuthError
from dotenv import load_dotenv
import io
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# SHOULD BE MOVED FROM HERE 

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory="../templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/' , response_class=HTMLResponse)
def home(request : Request):
    '''
    Homepage Template
    '''
    return templates.TemplateResponse("home.html" , {"request" : request})

@app.post('/create' , status_code=201)
async def handle_form(request : Request ,class_name : str = Form(...) , instructor_name : str = Form(...)  ,db : Session = Depends(get_db)):
    date_time = datetime.now()
    new_session = models.Class(class_name= class_name , instructor_name= instructor_name , date_time=date_time)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    session_id = new_session.id
    return RedirectResponse(url=f'/qr/{session_id}')
    #return qr(request , new_session.id , new_session.class_name , new_session.instructor_name) #templates.TemplateResponse("session.html" , {'request' : request})


# @app.get('/data',response_class=HTMLResponse)
# def show_data(id:int):
#     pass

@app.post('/qr/{id}')
def show_qr(request: Request, id:str ):

    auth_link = f"/qr/{id}/login"
    img = qrcode.make(auth_link)
    img.save("img.png")
    print(img.save("img.png"))
    return templates.TemplateResponse('session.html', { 'request' : request , 'qr_img' : '../app/img.png'})
    #return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
# def gen_qr(auth_link):
#     img = qrcode.make(auth_link)
#     #qr_img = img.save("img.png")
#     return StreamingResponse(io.BytesIO(img.tobytes()), media_type="image/png")
# @app.get('/csv')
# def make_csv(id:int):
#     #Qurey from data base
#     pass


@app.route('/qr/{id}/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/qr')















# @app.post('/attendace',response_class=HTMLResponse)
# def add_student(id:int):
#     pass

# @app.get('/session' , response_model=schemas.Session , response_class=HTMLResponse)
# def session(request : Request):
#     course_name = 'course_1'
#     instructor = "instructor_1"
#     return templates.TemplateResponse("session.html" , {"request" : request , "course_name" : course_name , 'instructor_name' : instructor})

# @app.post("/student")
# async def student_form(request : forms.StudentForm):
#     print(request)


