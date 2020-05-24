#!/usr/bin/env python

from flask import render_template, request, session, redirect, Response
# from . import main

from ..models import *
from flask_login import login_required,current_user
from flask import Blueprint

from ..DatabaseOperations import DatabaseOperations


adminBlue = Blueprint('admin',__name__)



@adminBlue.route('/index',methods=['POST','GET'])
@login_required
def admin_home():
    if request.method == 'GET':

        return render_template('admin_home.html')

#课程查询列表
@adminBlue.route('/course',methods=['POST','GET'])
@login_required
def admin_course():
    if request.method == 'GET':
        courseId=request.args.get("courseId")
        if courseId is None or courseId=="":
            return render_template('admin_course.html')
        #查询课程信息
        databaseOperation=DatabaseOperations()
        sql=" SELECT c.id,c.`name`,st.`name`,st.id FROM stud_course as s LEFT JOIN course as c ON s.course_id=c.id LEFT JOIN student as st ON s.student_id=st.id WHERE c.id=%s"
        courselst=databaseOperation.select_many(sql,(courseId))

        if len(courselst) ==0:
            sql="SELECT c.id, c.`name` FROM course AS c  WHERE c.id =%s"
            courselst = databaseOperation.select_many(sql, (courseId))

        return render_template('admin_course.html',courselst=courselst,course_id=courseId)


@adminBlue.route("/course/delete",methods=["GET"])
def admin_course_delete():
    if request.method == 'GET':
        id = request.args.get("id")
        teacherId = request.args.get("teacherId")
        # 删除老师的某一个课程
        databaseOperation = DatabaseOperations()
        sql = 'delete from course where id=%s'
        databaseOperation.delete(sql, (id))
        sql = 'delete from stud_course where id=%s'
        databaseOperation.delete(sql, (id))
        return redirect("/admin/course")

@adminBlue.route('/course/add',methods=['POST','GET'])
@login_required
def admin_course_add():
    if request.method == 'GET':
        return render_template('add_course.html')

    else:
        id=request.form.get("id")
        name=request.form.get("name")
        week=request.form.get("week")
        time=request.form.get("time")
        week_time=week+time
        databaseOperation=DatabaseOperations()
 #查询添加的课程id是否存在
        sql ="select * from course where  id=%s"
        row=databaseOperation.select_one(sql,(id))
        if row is not None:
            return render_template('add_course.html',message="该课程ID已经存在")

        #插入课程信息
        sql="insert into course(id,name,time) values (%s,%s,%s)"
        databaseOperation.insert_one(sql,(id,name,week_time))

        return redirect("/admin/course")

@adminBlue.route('/course/edit',methods=['POST','GET'])
@login_required
def admin_course_edit():
    courseId =request.args.get("courseId")
    studentId=request.args.get("studentId")
    if request.method == 'GET':
        #查询课程某一条学生的信息数据

        sql="""SELECT c.id,c.`name`,st.`name`,st.id FROM stud_course as s LEFT JOIN course as c ON s.course_id=c.id LEFT JOIN student as st ON s.student_id=st.id WHERE c.id=%s and st.id=%s"""
        databaseOperation=DatabaseOperations()


        row=databaseOperation.select_one(sql,(courseId,studentId))

        return render_template('edit_course_student.html',result=row)



    else:
        courseName = request.form.get("name")

        databaseOperation = DatabaseOperations()
        #获取要更改的信息，并用sql更新数据库

        if courseName is not None and courseName !="":

            sql="update course set name=%s where id =%s"
            databaseOperation.update(sql,(courseName,courseId))

        return redirect("/admin/course?courseId="+str(courseId))

#教师页面
@adminBlue.route('/teacher',methods=['POST','GET'])
@login_required
def admin_teacher():
    if request.method == 'GET':
        teacher_id=request.args.get("teacherId")
        if teacher_id is None or teacher_id=="":
            return render_template('admin_teacher.html', teacherlst=[])

        #查询某个老师的所有课程信息

        databaseOperation=DatabaseOperations()
        sql='select t.name,t.id,t.age,ifnull(t.salary,0), c.name AS course_name,c.id from teacher as t LEFT JOIN course as c on c.teacher_id=t.id where t.id=%s '
        rows = databaseOperation.select_many(sql, (teacher_id))
        return render_template('admin_teacher.html',teacherlst=rows,teacher_id=teacher_id)




@adminBlue.route('/teacher/delete',methods=['POST','GET'])
@login_required
def admin_teacher_delete():
    if request.method == 'GET':
        id=request.args.get("id")
        teacherId=request.args.get("teacherId")
        #删除老师的某一个课程
        databaseOperation=DatabaseOperations()
        sql='delete from stud_course where course_id=%s'
        databaseOperation.delete(sql,(id))
        sql='update course set teacher_id=%s where id=%s'
        databaseOperation.update(sql,(None,None,id))
        return redirect("/admin/teacher?teacherId="+teacherId)


@adminBlue.route('/teacher/edit',methods=['POST','GET'])
@login_required
def admin_teacher_edit():
    teacher_id = request.args.get("teacherId")
    #查询老师的个人信息
    if request.method == 'GET':
        databaseOperation=DatabaseOperations()
        sql='select * from teacher where id=%s'
        rows=databaseOperation.select_one(sql,(teacher_id))
        return render_template('edit_teacher_info.html',row=rows)
    # 获取相关信息，并更新数据库
    password=request.form.get("password")
    name=request.form.get("name")
    age=request.form.get("age")
    graduation_school=request.form.get("graduation_school")

    sql="update teacher set password=%s,name=%s,age=%s,graduation_school=%s where id=%s"
    databaseOperation = DatabaseOperations()
    databaseOperation.update(sql,(password,name,age,graduation_school,teacher_id))
    return redirect("/admin/teacher?teacherId="+teacher_id)
#为老师添加课程
@adminBlue.route('/teacher/add',methods=['POST','GET'])
@login_required
def admin_teacher_add_course():
    teacher_id = request.args.get("teacherId")

    if request.method == 'GET':

        #查询还没有老师教课的课程
        databaseOperation=DatabaseOperations()
        sql='select id,name FROM course WHERE teacher_id =0'
        rows=databaseOperation.select_many(sql,())
        return render_template('add_course_for_teacher.html',row=rows)
    #获取前端的课程id，并绑定为该老师教课
    courseId=request.form.getlist("courseId")
    databaseOperation = DatabaseOperations()

    sql="update course set teacher_id=%s where id=%s"
    for i in courseId:
        databaseOperation.update(sql,(teacher_id,i))
    return redirect("/admin/teacher?teacherId="+teacher_id)

#获取学生相关信息
@adminBlue.route('/student',methods=['POST','GET'])
@login_required
def admin_student():
    if request.method == 'GET':
        student_id=request.args.get("studentId")
        if student_id is None or student_id == "":
            return render_template('admin_student.html', teacherlst=[])

        databaseOperation=DatabaseOperations()
        sql='select s.name,s.id,s.age,s.gender,s.phone_number,  c.course_name,c.id AS course_name from student as s LEFT JOIN stud_course as c on c.student_id=s.id where s.id=%s'
        rows=databaseOperation.select_many(sql,(student_id))
        return render_template('admin_student.html',studentlst=rows,student_id=student_id)

#删除学生的某一门课程
@adminBlue.route('/student/delete',methods=['POST','GET'])
@login_required
def admin_student_delete():
    if request.method == 'GET':
        id=request.args.get("id")
        student_id=request.args.get("studentId")
        databaseOperation=DatabaseOperations()
        sql='delete from stud_course where id=%s'
        databaseOperation.delete(sql,(id))
        return redirect("/admin/student?studentId="+student_id)

#编辑学生的个人信息
@adminBlue.route('/student/edit',methods=['POST','GET'])
@login_required
def admin_student_edit():
    student_id = request.args.get("studentId")

    if request.method == 'GET':
        databaseOperation=DatabaseOperations()
        sql='select * from student where id=%s'
        rows=databaseOperation.select_one(sql,(student_id))
        return render_template('edit_student_info.html',row=rows)
    #获取相关修改信息，并更新数据库
    password=request.form.get("password")
    name=request.form.get("name")
    age=request.form.get("age")
    phone_number=request.form.get("phone_number")

    sql="update student set password=%s,name=%s,age=%s,phone_number=%s where id=%s"
    databaseOperation = DatabaseOperations()
    databaseOperation.update(sql,(password,name,age,phone_number,student_id))
    return redirect("/admin/student?studentId="+student_id)
#为学生添加课程
@adminBlue.route('/student/add',methods=['POST','GET'])
@login_required
def admin_student_add_course():
    student_id = request.args.get("studentId")

    if request.method == 'GET':
        #查询学生还没有报名的科目
        databaseOperation=DatabaseOperations()
        sql='select id,name FROM course WHERE id not in (select course_id FROM stud_course  WHERE  student_id=%s) AND `name` NOT IN (select `name` FROM course LEFT JOIN stud_course on stud_course.course_id=course.id WHERE stud_course.student_id=%s)'
        rows=databaseOperation.select_many(sql,(student_id,student_id))
        return render_template('add_course_for_student.html',row=rows)
    #循环便利要为学生添加的科目
    courseId=request.form.getlist("courseId")
    databaseOperation = DatabaseOperations()

    #插入数据

    sql="insert into stud_course(student_id,course_id,course_name) values(%s,%s,%s)"
    for i in courseId:
        id,name=i.split('&')
        databaseOperation.insert_one(sql,(student_id,id,name))
    return redirect("/admin/student?studentId="+student_id)


