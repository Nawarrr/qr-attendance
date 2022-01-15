from fastapi import FastAPI , Request, Form , Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import qrcode
#import forms 
from datetime import datetime 
#import pandas as pd 
import schemas ,models
from database import engine , SessionLocal
from sqlalchemy.orm.session import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

    return qr(new_session.id , new_session.class_name , new_session.instructor_name) #templates.TemplateResponse("session.html" , {'request' : request})


@app.get('/data',response_class=HTMLResponse)
def show_data(id:int):
    pass

@app.get('/qr',response_class=HTMLResponse )
def qr(id:int,class_name:str ,instructor_name:str ,request:Request):

    auth_link = " ZBI "
    qr_img = qrcode.make(auth_link)
    return templates.TemplateResponse('session.html', {'request' : request , 'class_name' : class_name , 'instructor_name' : instructor_name})
    

@app.get('/csv')
def make_csv(id:int):
    #Qurey from data base
    pass

@app.post('/attendace',response_class=HTMLResponse)
def add_student(id:int):
    pass

# @app.get('/session' , response_model=schemas.Session , response_class=HTMLResponse)
# def session(request : Request):
#     course_name = 'course_1'
#     instructor = "instructor_1"
#     return templates.TemplateResponse("session.html" , {"request" : request , "course_name" : course_name , 'instructor_name' : instructor})

# @app.post("/student")
# async def student_form(request : forms.StudentForm):
#     print(request)