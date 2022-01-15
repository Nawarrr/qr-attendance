from fastapi import FastAPI , Request, Form , Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import qrcode
#import forms 
from datetime import datetime 
#import csv
import schemas ,models
from database import engine , SessionLocal
from sqlalchemy.orm.session import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


templates = Jinja2Templates(directory="templates")

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
    # Auth2
    auth_link = " ZBI "
    qr_img = qrcode.make(auth_link)
    return templates.TemplateResponse('session.html', {'request' : request , 'class_name' : class_name , 'instructor_name' : instructor_name , 'qr_img' : qr_img})
    

# @app.get('/csv')
# def make_csv(id:int):
#     #Qurey from data base into dict 
#     labels = ['First Name','Last Name','E-mail','Date']
#     with open(f'{id}.csv', 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames = labels)
#         writer.writeheader()
#         writer.writerows(cars)

@app.post('/attendace',response_class=HTMLResponse)
def add_student(id:int):
    pass



# @app.post("/student")
# async def student_form(request : forms.StudentForm):
#     print(request)