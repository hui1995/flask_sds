import os
from datetime import time, datetime

from flask import render_template, request, session, redirect, Response
from ..models import *
from flask_login import login_user,login_required,logout_user
from flask import Blueprint
from ..DatabaseOperations import *
mainBlu = Blueprint('main',__name__)



#登陆接口
@mainBlu.route('/',methods=['POST','GET'])
@mainBlu.route('/login',methods=['POST','GET'])
def login_views():
    if request.method == 'GET':
        return render_template('login_interface.html')
    #获取用户名密码和类型
    username = request.form['username']
    password = request.form['password']
    type=request.form['type']

    #判断是否输入用户名
    if username is None or username == "" or password is None or password == "":
        return render_template('login_interface.html', message="用户名或者密码为空")
#判断是否记住密码
    try:
        remeber_me=request.form['remeber_me']
        if remeber_me == "on":
            remeber_me = True
        else:
            remeber_me = False
    except:
        remeber_me=False
    databaseOperations = DatabaseOperations()
    #如果类型为3，则管理员登陆校验
    if int(type)==3:
        if username=='admin' and password=="admin":
            user = User(0, 'admin', 'admin')
            login_user(user)
            session['user_type']=int(3)
            return redirect("/admin/index")

        #如果为2，则是教师登陆
    elif int(type)==2:
        #查询该教师是否存在
        sql = "select id,name,password from teacher where account=%s"
        row=databaseOperations.select_one(sql,(username))
        #如果不存在，则提示
        if row is None:
            return render_template('login_interface.html', message="该教师不存在")
        else:
            #如果存在，则对比密码
            if row[2]!=password:
                return render_template('login_interface.html', message="登陆密码不正确")
            else:
                #密码正确，则实力化一个user对象，并运用login_user方法进行状态保持
                user=User(row[0],row[1],row[2])
                session['user_type'] = int(type)
                login_user(user,remeber_me)
                return redirect("/teacher/index")
    #学生登陆（业务逻辑跟教师一样）
    else:
        sql = "select id,name,password from student where account=%s"
        row = databaseOperations.select_one(sql, (username))
        if row is None:
            return render_template('login_interface.html', message="该学生不存在")
        else:
            if row[2] != password:
                return render_template('login_interface.html', message="登陆密码不正确")
            else:
                user=User(row[0],row[1],row[2])
                login_user(user, remeber_me)
                session['user_type'] = int(type)
                return redirect("/student/index")

    return render_template('login_interface.html')
#注册老师
@mainBlu.route('/signup/teacher',methods=['GET',"POST"])
def signUpTeacher():
    if request.method=="GET":
        return render_template('teacher_signup_interface.html')

    else:
        #获取相关信息
        account = request.form['username']
        name = request.form['name']
        gender = request.form['gender']
        graduation_school = request.form['graduation_school']
        age = request.form['age']
        password = request.form['password']
        password2 = request.form['password2']
        #判断密码是否正确
        if password is None or password !=password2:
            return render_template('teacher_signup_interface.html',message="密码填写不完整或两次密码不一致")
        #判断相关信息是否为空
        elif account is None or account=="" or name is None or name=="" or gender is None or gender=="" or graduation_school is None or graduation_school=="" and age is None or age =="":
            return render_template('teacher_signup_interface.html',message="信息填写不完整")
        #查询该账号是否已经注册
        databaseOperations = DatabaseOperations()
        sql="select id from teacher where account=%s"
        result=databaseOperations.select_one(sql,(account))
        if result is None:
            #如果没有注册，则注册成功

            sql = "insert into teacher(account,name,gender,age,graduation_school,password) values(%s,%s,%s,%s,%s,%s)"
            databaseOperations.insert_one(sql, (account, name, gender, age, graduation_school, password))
        else:
            return render_template('teacher_signup_interface.html',message="该用户已经存在")

        return redirect("/login")
#学生注册，跟老师注册流程一致
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
        databaseOperations = DatabaseOperations()
        sql = "select id from student where account=%s"

        result = databaseOperations.select_one(sql, (account))
        if result is None:
            sql ="insert into student(account,name,gender,age,phone_number,password) values(%s,%s,%s,%s,%s,%s)"
            databaseOperations.insert_one(sql,(account,name,gender,age,phone_number,password))
        else:
            return render_template('student_page_related_class.html',message="该用户已经存在")

        return redirect("/login")



#登出
@mainBlu.route('/logout')  # 登出
@login_required
def logout():
    #删除session
    logout_user()
    del session['type']
    return redirect('/login')



