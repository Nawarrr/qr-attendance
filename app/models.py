from sqlalchemy import  Column, Integer, String, DateTime , ForeignKey
from .database import Base
from sqlalchemy.orm import relationship



class Class(Base):
    __tablename__ = 'classs'

    id = Column(Integer, primary_key=True , index= True)
    date_time = Column(DateTime)
    class_name = Column(String)
    instructor_name = Column(String)

    instructor = relationship('Student' , back_populates='classs')


class Student(Base):
    __tablename__ = 'student'

    student_id = Column(Integer, primary_key=True , index= True)
    student_name = Column(String)
    student_info =  Column(String)
    class_id = Column(Integer, ForeignKey('classs.id'))
    
    classs = relationship('Class' , back_populates='instructor')