import os
from datetime import time, datetime

from flask import render_template, request, session, redirect, Response
from ..models import *
from flask_login import login_user,login_required,logout_user
from flask import Blueprint
mainBlu = Blueprint('main',__name__)


@mainBlu.route('/login',methods=['POST','GET'])
def login_views():
    if request.method == 'GET':

        return render_template('login_interface.html')
    username = request.form['username']
    password = request.form['password']
    type=request.form['type']


    if username is None or username == "" or password is None or password == "":
        return render_template('login_interface.html', message="用户名或者密码不正确")

    try:
        remeber_me=request.form['remeber_me']
        if remeber_me == "on":
            remeber_me = True
        else:
            remeber_me = False
    except:
        remeber_me=False
    if int(type)==3:
        if username=='admin' and password=="admin":
            admin=Admin()
            login_user(admin)
            session['type']=int(3)
            return redirect("/admin/index")
    elif int(type)==2:
        teacher=Teacher.query.filter(Teacher.account==username).first()
        if teacher is None:
            return render_template('login_interface.html', message="该教师不存在")
        else:
            if teacher.password!=password:
                return render_template('login_interface.html', message="登陆密码不正确")
            else:

                login_user(teacher,remeber_me)
                session['type']=int(type)
                return redirect("/teacher/index")
    else:
        student = Student.query.filter(Student.account == username).first()
        if student is None:
            return render_template('login_interface.html', message="该学生不存在")
        else:
            if student.password != password:
                return render_template('login_interface.html', message="登陆密码不正确")
            else:

                login_user(student, remeber_me)
                session['type'] = int(type)
                return redirect("/student/index")





    return render_template('login_interface.html')

@mainBlu.route('/signup/teacher',methods=['GET',"POST"])
def signUpTeacher():
    if request.method=="GET":
        return render_template('teacher_signup_interface.html')

    else:


        account = request.form['username']
        name = request.form['name']
        gender = request.form['gender']
        graduation_school = request.form['graduation_school']
        age = request.form['age']
        password = request.form['password']
        password2 = request.form['password2']
        if password is None or password !=password2:
            return render_template('teacher_signup_interface.html',message="密码填写不完整或两次密码不一致")
        elif account is None or account=="" or name is None or name=="" or gender is None or gender=="" or graduation_school is None or graduation_school=="" and age is None or age =="":
            return render_template('teacher_signup_interface.html',message="信息填写不完整")

        student=Student()
        student.account=account
        student.name=name
        student.gender=gender
        student.graduation_school=graduation_school
        student.password=password
        db.session.add(student)
        return redirect("/login")

@mainBlu.route('/signup/student',methods=['GET',"POST"])
def signUpStudent():
    if request.method == "GET":
        return render_template('student_signup_interface.html')

    else:


        account = request.form['username']
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        phone_number = request.form['phone_number']
        password = request.form['password']
        password2 = request.form['password2']
        if password is None or password !=password2:
            return render_template('student_page_related_class.html',message="密码填写不完整或两次密码不一致")
        elif account is None or account=="" or name is None or name=="" or gender is None or gender=="" or age is None or age=="" :
            return render_template('student_page_related_class.html',message="信息填写不完整")

        student=Student()
        student.account=account
        student.name=name
        student.gender=gender
        student.age=age
        student.phone_number=phone_number
        student.password=password
        db.session.add(student)
        return redirect("/login")




@mainBlu.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    del session['type']
    return redirect('/login')



