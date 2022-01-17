
from fastapi import APIRouter , Request , Form , Depends

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm.session import Session
from logic.student import student_attendance

import database

router = APIRouter(
    tags=['student'],
    prefix="/student"
)

templates = Jinja2Templates(directory="../templates")


@router.get('/{id}' )
def student_page(request:Request):
    """

    :param request:Request: 

    """
    return templates.TemplateResponse("student.html" , {"request" : request})


@router.post('/{id}' )
def student_form(request : Request,  id : int   ,student_name : str = Form(...) , student_info : str = Form(...),db : Session = Depends(database.get_db) ):
    """

    :param request : Request: 
    :param id : int: 
    :param student_name : str:  (Default value = Form(...))
    :param student_info : str:  (Default value = Form(...))
    :param db : Session:  (Default value = Depends(database.get_db))

    """
    student_attendance(id, student_name,student_info,db)
    return templates.TemplateResponse("thankyou.html" , {'request' : request})
