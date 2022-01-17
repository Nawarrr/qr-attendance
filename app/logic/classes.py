from datetime import datetime
import models
import os
import qrcode
import pandas as pd


def insert_class_toDB(class_name:str , instructor_name:str , db):
    date_time = datetime.now()
    new_session = models.Class(class_name= class_name , instructor_name= instructor_name , date_time=date_time) 
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    url = os.environ.get('URL')
    auth_link = f"{url}/login/{new_session.id}"

    img = qrcode.make(auth_link)
    img.save("img.png")
    return new_session.id , auth_link

def query_create_csv(id:int,db):

    records = db.query(models.Student).filter(models.Student.class_id==id).all()

    df = pd.DataFrame(columns= ['Student Name' , 'Student Info'] )
    for i ,record in enumerate(records):
        df.loc[i]= [ record.student_name , record.student_info] 

    
    return df.to_csv('../templates/attendance.csv')