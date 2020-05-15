
from . import db
from flask_login import UserMixin

class Admin( UserMixin):
    id=1
    name='admin'
    password="admin"

class Student(db.Model,UserMixin):
    __tablename__ = 'student'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(250),nullable=False)
    gender = db.Column(db.Integer,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    account=db.Column(db.String(50),nullable=False)
    phone_number = db.Column(db.Integer,nullable=False)


class Teacher(db.Model,UserMixin):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(250),nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    account=db.Column(db.String(50),nullable=False)
    age = db.Column(db.Integer,nullable=False)

    graduation_school = db.Column(db.String(50), nullable=False)



class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    teacher_name = db.Column(db.String(50), nullable=False)
    the_newest_chapter=db.Column(db.Integer, nullable=False)
    rest_class=db.Column(db.Integer, nullable=False)
    time=db.Column(db.String(50))

class StudCourse(db.Model):
    __tablename__ = 'stud_course'
    id = db.Column(db.Integer, primary_key=True)
    student_id=db.column(db.Integer)
    course_id=db.column(db.Integer)





