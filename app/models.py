from datetime import datetime
from sqlite3 import Date
from sqlalchemy import  Column, Integer, String, DateTime , ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment


class Class(Base):
    __tablename__ = 'classs'

    
    id = Column(Integer, primary_key=True , index= True)
    date_time = Column(DateTime)
    class_name = Column(String)
    instructor_name = Column(String)
    #qr_picture = image_attachment('ClassQR')
    instructor = relationship('Student' , back_populates='classs')

# class ClassQR(Base, Image):
#     __tablename__ = 'class_qr'

#     classs_id = Column(Integer, ForeignKey('classs.id'), primary_key=True)
#     classs = relationship('Class')


class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True , index= True)
    student_name = Column(String)
    student_info =  Column(String)
    class_id = Column(Integer, ForeignKey('classs.id'))
    classs = relationship('Class' , back_populates='instructor')