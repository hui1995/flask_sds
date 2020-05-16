#!/usr/bin/env python

from flask import render_template, request, session, redirect, Response
# from . import main
from ..models import *
from flask_login import login_required,current_user
from flask import Blueprint
from ..DatabaseOperations import DatabaseOperations

teacherBlu = Blueprint('teacher',__name__)
#教师主页面
@teacherBlu.route('/index',methods=['POST','GET'])
@login_required
def teacher_home():
    if request.method == 'GET':
        return render_template('teacher-home.html')

#个人信息页面
@teacherBlu.route('/person',methods=['POST','GET'])
@login_required
def teacher_person():
    if request.method == 'GET':
        #根据当前用户的id查询个人信息
        databaseOperations=DatabaseOperations()
        sql='select * from teacher where id=%s'
        teacher=databaseOperations.select_one(sql,(current_user.id))

        return render_template('teacher-personal.html',teacher=teacher)

#课程页面
@teacherBlu.route('/course',methods=['POST','GET'])
@login_required
def teacher_course():
    if request.method == 'GET':
        #根据当前登陆用户的信息查询其教的课程
        databaseOperations = DatabaseOperations()
        sql = 'select * from course where teacher_id=%s'
        courselst = databaseOperations.select_many(sql, current_user.id)
        return render_template('teacher-courses.html',userinfo=current_user,courselst=courselst)


#添加咨询页面
@teacherBlu.route('/add/inform',methods=['POST','GET'])
@login_required
def informAdd():
    id = request.args["id"]

    if request.method == 'GET':
        return render_template('add_information.html',id=id)
    else:
        #获取前端的信息
        information=request.form.get("information")
        #插入数据库
        sql="insert into inform(class_id,information) values(%s,%s)"
        databaseOperations = DatabaseOperations()
        databaseOperations.insert_one(sql,(id,information))
        return redirect("/teacher/course")

#获取学生信息列表
@teacherBlu.route('/stu/list',methods=['POST','GET'])
@login_required
def teacher_course_student_list():
    if request.method == 'GET':
        id =request.args['id']
        databaseOperations = DatabaseOperations()


    #查询当前课程的学生的信息
        sql = "select s.id as id,s.name as name,s.age as age, s.gender as gender from `stud_course` as c left join student as s on c.student_id=s.id where c.course_id=%s";
        result = databaseOperations.select_many(sql,(id))

        return render_template('teacher-course-student.html',userinfo=current_user,result=result)

#当前章节签到
@login_required
@teacherBlu.route('/stu/attend',methods=['POST','GET'])
def teacher_course_student_list_attend():
    if request.method == 'GET':
        id =request.args['id']
        databaseOperations = DatabaseOperations()

        #查询当前最新章节的签到情况
        sql = """
               select 
s.id,
s.name,

s.age AS age,
	s.gender AS gender ,
	s.chapter+1 as chapter,
	i.is_attendance as attendance
FROM(


SELECT
	s.id AS id,
	s.NAME AS NAME,
	s.age AS age,
	s.gender AS gender ,
	course.the_newest_chapter as chapter
FROM
	`stud_course` AS c
	LEFT JOIN student AS s ON c.student_id = s.id RIGHT JOIN course on course.id=c.course_id
WHERE
	c.course_id =%s) as s LEFT JOIN attendance  as i on (i.student_id)=s.id and i.chapter=s.chapter+1"""
        result = databaseOperations.select_many(sql, (id))


        #查询下一节应该是多少节课
        sql="select name,the_newest_chapter+1 from course where id=%s "
        courseInfo = databaseOperations.select_one(sql, (id))
        #如果大于20，则标记为完成
        if courseInfo>20:
            return render_template('teacher-courses-current-attendance.html', message="该课程已经完结")

        return render_template('teacher-courses-current-attendance.html',userinfo=current_user,id=id,result=result,courseInfo=courseInfo)
#标记学生的出席情况
@login_required
@teacherBlu.route('/check/attend',methods=['POST','GET'])
def attend_check():
    if request.method == 'GET':
        id =request.args['courseId']
        student_id=request.args['studentId']
        isAttend=request.args['is_attend']#1是出席，0是未出席
        #查询最新的章节是第几节
        sql="select the_newest_chapter from course where id=%s "
        databaseOperations = DatabaseOperations()
        row=databaseOperations.select_one(sql,(id))
        #将学生签到情况，加入数据库
        sql = "insert into attendance(course_id,student_id,is_attendance,chapter) values (%s,%s,%s,%s)"
        databaseOperations.insert_one(sql, (id,student_id,isAttend,row[0]+1))
        return redirect("/teacher/stu/attend?id="+str(id))
#当前章节签到完毕，提交一下
from datetime import date
@login_required
@teacherBlu.route('/check/end',methods=['POST','GET'])
def attend_check_end():
    if request.method == 'GET':
        id =request.args['courseId']
        #签到完毕，课程的学习进度加一
        sql="""update
 course SET the_newest_chapter=the_newest_chapter+1,rest_class-1
 WHERE id=%s"""
        databaseOperations = DatabaseOperations()

        databaseOperations.insert_one(sql, (id))

        #老师工资加50

        sql="update teacher set salary=salary+50 where id=%s"
        databaseOperations.insert_one(sql, current_user.id)
        #查询老师工资的最新一条记录

        sql="select teacher_id,rest from salary where teacher_id=%s order by id"
        row=databaseOperations.select_one(sql,current_user.id)
        if row==None:
            row=[current_user.id[0],0]
        #存入一条老师收入记录
        sql="insert into salary(teacher_id,date,income_outcome,rest) values(%s,%s,%s,%s)"
        databaseOperations.insert_one(sql,(current_user.id[0],date.today(),50,row[1]+50))

        return redirect("/teacher/stu/attend?id="+str(id))

#历史出席记录
@login_required
@teacherBlu.route('/history/list/attend', methods=['POST', 'GET'])
def history_list_attend():

    if request.method=="GET":
        databaseOperations = DatabaseOperations()
        #根据老师查询课程

        sql="select id,name,the_newest_chapter from course where teacher_id=%s"
        resulst=[]
        #循环每一个课程
        rows=databaseOperations.select_many(sql,current_user.id)
        for i in rows:
            dict1={}
            dict1["course"]=i[1]
            detail=[]
            #i[2]为每一个课程的最新章节，记录一下，循环查询一下每个章节的签到状态
            for x in range(1,i[2]+1):
                dict2={}
                dict2['chapter']="第"+str(x)+"章节"
                sql="""select a.is_attendance,s.id,s.name,a.chapter FROM attendance as a LEFT JOIN student as s on s.id=a.student_id WHERE a.course_id=%s AND a.chapter=%s """
                info=databaseOperations.select_many(sql,(i[0],x))
                dict2["detail"]=info
                detail.append(dict2)
            dict1['detail']=detail
            resulst.append(dict1)
        return render_template('teacher-attendance.html',resulst=resulst)

#查询工资信息
@login_required
@teacherBlu.route('/salary', methods=['POST', 'GET'])
def salary():
    if request.method=="GET":
        #根据教师id查询工资
        databaseOperations = DatabaseOperations()
        sql="select salary from teacher where id =%s"
        row=databaseOperations.select_one(sql,current_user.id)
        return render_template('teacher-salary.html',result=row)


#工资提现
@login_required
@teacherBlu.route('/salary/out', methods=['POST', 'GET'])
def salaryOut():
    if request.method=="POST":
        salary=request.form['salary']
        databaseOperations = DatabaseOperations()
        #查询工资剩余额度
        sql = "select salary from teacher where id =%s"
        row = databaseOperations.select_one(sql, current_user.id)
        salary=float(salary)
        #如果提现工资小于0，或者大于工资总额，则不允许提现
        if salary<=0 or float(salary)>row[0]:
            return render_template('teacher-salary.html',result=row, message="不能为0或者负数")

        #，更新剩余工资
        sql="update teacher set salary=%s where id=%s"
        databaseOperations.insert_one(sql,(float(row[0])-salary,current_user.id))
        #查询最后一条工资记录
        sql="select teacher_id,rest from salary where teacher_id=%s order by id"
        row=databaseOperations.select_one(sql,current_user.id)
        if row==None:
            row=[current_user.id[0],0]
        #加一条工资记录
        sql="insert into salary(teacher_id,date,income_outcome,rest) values(%s,%s,%s,%s)"
        databaseOperations.insert_one(sql,(current_user.id[0],date.today(),-salary,float(row[1])-salary))
        return redirect('/teacher/salary')