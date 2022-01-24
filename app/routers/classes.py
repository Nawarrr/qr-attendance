from fastapi import APIRouter , Request , Form , Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from logic.classes import insert_class_toDB , query_create_csv
import   database
from sqlalchemy.orm.session import Session






router = APIRouter(
    tags=['instructor']
)
templates = Jinja2Templates(directory="../templates")


@router.get('/' , response_class=HTMLResponse)
def home(request : Request):
    """Homepage Template

    :param request : Request: 

    """
    return templates.TemplateResponse("home.html" , {"request" : request})




@router.post('/create' , status_code=201)
def handle_form(request : Request ,class_name : str = Form(...) , instructor_name : str = Form(...)  ,db : Session = Depends(database.get_db)):
    """

    :param request : Request: 
    :param class_name:str:
    :param instructor_name:str: 
    :param db : Session:  (Default value = Depends(database.get_db))

    """
    
    new_session_id , auth_link , img_tag = insert_class_toDB(class_name , instructor_name , db)

    return templates.TemplateResponse("session.html" , {'request' : request , "id" : new_session_id , 'img' : img_tag , 'link' : auth_link} )




@router.get('/create' , tags=['instructor'])
def show_session(request: Request):
    """

    :param request: Request: 

    """
    return templates.TemplateResponse("session.html" , {'request' : request})


@router.post('/download/{id}' , tags=['instructor'])
def download_csv(request : Request, id:int ,db : Session = Depends(database.get_db)):
    """

    :param request : Request: 
    :param id:int: 
    :param db : Session:  (Default value = Depends(database.get_db))

    """
    query_create_csv(id , db)

    return templates.TemplateResponse("session.html" , {'request' : request})