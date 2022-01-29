
from fastapi import APIRouter, Request, Form, Depends
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm.session import Session
from logic.student import take_student_attendance
from .auth import login
import database


router = APIRouter(
    tags=['student'],
    prefix="/student"
)

templates = Jinja2Templates(directory="../templates")


@router.get('/{id}')
def student_page(request: Request, id: int):
    """

    :param request:Request: 

    """
    return templates.TemplateResponse("student.html", {"request": request, "session_id": id})


@router.post('/{id}')
async def student_form(request: Request,  id: int, student_name: str = Form(...), student_info: str = Form(...), db: Session = Depends(database.get_db)):
    """

    :param request : Request: 
    :param id : int: 
    :param student_name : str:  (Default value = Form(...))
    :param student_info : str:  (Default value = Form(...))
    :param db : Session:  (Default value = Depends(database.get_db))

    """

    take_student_attendance(id, student_name, student_info, db)
    return templates.TemplateResponse("thankyou.html", {'request': request})
