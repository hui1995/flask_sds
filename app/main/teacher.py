#!/usr/bin/env python

from flask import render_template, request, session, redirect, Response
# from . import main
from .. import db
from ..models import *
from flask_login import login_required,current_user
from flask import Blueprint

teacherBlu = Blueprint('teacher',__name__)

@teacherBlu.route('/index',methods=['POST','GET'])
@login_required
def teacher_home():
    if request.method == 'GET':
        return render_template('teacher-home.html')


@teacherBlu.route('/person',methods=['POST','GET'])
@login_required
def teacher_person():
    if request.method == 'GET':
        teacher=Teacher.query.filter(Teacher.id==current_user.id).first()
        return render_template('teacher-personal.html',teacher=teacher)


@teacherBlu.route('/course',methods=['POST','GET'])
@login_required
def teacher_course():
    if request.method == 'GET':
        courselst=Course.query.filter(Course.teacher_id==current_user.id).all()
        return render_template('teacher-courses.html',userinfo=current_user,courselst=courselst)


@teacherBlu.route('/stu/list',methods=['POST','GET'])
@login_required
def teacher_course_student_list():
    if request.method == 'GET':
        id =request.args['id']

        sql = "select s.name as name,s.age as age, s.gender as gender from `stud_course` as c left join student as s on c.student_id=s.id where c.course_id='"+str(id)+"'";
        result = db.session.execute(sql).fetchall()


        return render_template('teacher-course-student.html',userinfo=current_user,result=result)

@login_required
@teacherBlu.route('/stu/attend',methods=['POST','GET'])

def teacher_course_student_list_attend():
    if request.method == 'GET':
        id =request.args['id']

        sql = "select s.id,s.name as name,s.age as age, s.gender as gender from `stud_course` as c left join student as s on c.student_id=s.id where c.course_id='"+str(id)+"'";
        result = db.session.execute(sql).fetchall()


        return render_template('teacher-courses-current-attendance.html',userinfo=current_user,result=result)

