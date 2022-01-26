import models

def take_student_attendance(id:int, student_name:str , student_info:str , db):
    """

    :param id:int: 
    :param student_name:str: 
    :param student_info:str: 
    :param db: sqlalchemy.orm.session 
 
     """
    new_session = models.Student(student_name= student_name ,  student_info= student_info , class_id=id )
    db.add(new_session)
    db.commit()
    
    return db.refresh(new_session)