from datetime import datetime
from .. import models
import os
import qrcode
import pandas as pd


def insert_class_toDB(class_name: str, instructor_name: str, db):
    """

    :param class_name:str: 
    :param instructor_name:str: 
    :param db: sqlalchemy.orm.session 

    """
    date_time = datetime.now()  # Time right now
    new_session = models.Class(
        class_name=class_name, instructor_name=instructor_name, date_time=date_time)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # get the URL of the website from env variables
    url = os.environ.get('URL')
    auth_link = f"{url}/student/{new_session.id}"
    img = qrcode.make(auth_link)
    img.save("././templates/img.png")

    return new_session.id, auth_link


def query_create_csv(id: int, db):
    """

     :param id:int: 
     :param db: sqlalchemy.orm.session

    """
    records = db.query(models.Student).filter(
        models.Student.class_id == id).all()

    df = pd.DataFrame(columns=['Student Name', 'Student Info'])
    # i is the index and record is the entry in DB
    for i, record in enumerate(records):
        # Adds a new row with every iteration
        df.loc[i] = [record.student_name, record.student_info]
    df.index = df.index + 1
    return df.to_csv('././templates/attendance.csv')
