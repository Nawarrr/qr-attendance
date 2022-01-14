from fastapi import FastAPI , Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import forms 

app = FastAPI()


templates = Jinja2Templates(directory="templates")


@app.get('/' , response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse("home.html" , {"request" : request})

@app.post('/submitform')
async def handle_form(course_name : str = Form(...) , instructor_name : str = Form(...)):
    print(course_name)


    


# @app.get('/session' , response_model=forms.InstructorForm)
# def session():
#     course_name = 'course_1'
#     instructor = "instructor_1"
#     return templates.TemplateResponse("session.html" , {"request" : request , "course_name" : course_name , 'instructor_name' : instructor})

# @app.post("/student")
# async def student_form(request : forms.StudentForm):
#     print(request)