from datetime import datetime
from sqlite3 import Date
from sqlalchemy import  Column, Integer, String, DateTime
from database import Base


class Class(Base):
    __tablename__ = 'classes'

    
    id = Column(Integer, primary_key=True , index= True)
    date_time = Column(DateTime)
    class_name = Column(String)
    instructor_name = Column(String)
