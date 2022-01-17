import models
def student_attendance(id:int, student_name:str , student_info:str , db):
    new_session = models.Student(student_name= student_name ,  student_info= student_info , class_id=id )
    db.add(new_session)
    db.commit()
    
    return db.refresh(new_session)