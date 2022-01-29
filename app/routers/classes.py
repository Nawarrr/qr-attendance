from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from logic.classes import insert_class_toDB, query_create_csv
import database
from sqlalchemy.orm.session import Session


router = APIRouter(
    tags=['instructor']
)
templates = Jinja2Templates(directory="../templates")


@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    """Homepage Template

    :param request : Request: 

    """
    return templates.TemplateResponse("home.html", {"request": request})


@router.post('/create', status_code=201)
def handle_form(request: Request, class_name: str = Form(...), instructor_name: str = Form(...), db: Session = Depends(database.get_db)):
    """

    :param request : Request: 
    :param class_name:str:
    :param instructor_name:str: 
    :param db : Session:  (Default value = Depends(database.get_db))

    """

    new_session_id, auth_link = insert_class_toDB(class_name, instructor_name, db)
    return templates.TemplateResponse("session.html", {'request': request, "id": new_session_id, 'link': auth_link,
                                                       'class_name': class_name, 'instructor_name': instructor_name})


@router.get('/img.png')
def show_session():
    return FileResponse('../templates/img.png')


@router.post('/download/{id}')
def create_csv(request: Request, id: int, db: Session = Depends(database.get_db)):
    """

    :param request : Request: 
    :param id:int: 
    :param db : Session:  (Default value = Depends(database.get_db))

    """
    query_create_csv(id, db)
    return "Attendance Sheet Created"


@router.get('/attendance.csv')
def download_csv():
    return FileResponse('../templates/attendance.csv')
