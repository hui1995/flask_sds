#!/usr/bin/env python

from flask import render_template, request, session, redirect, Response
# from . import main
from ..models import *
from flask_login import login_required, current_user
from flask import Blueprint
from ..DatabaseOperations import DatabaseOperations

studentBlue = Blueprint('student', __name__)


# 学生主页面接口
@studentBlue.route('/index', methods=['POST', 'GET'])
@login_required
def student_home():
    if request.method == 'GET':
        # 创建一个sql链接，查询学生相关信息
        databaseOperations = DatabaseOperations()
        sql = 'select * from student where id=%s'
        student = databaseOperations.select_one(sql, current_user.id)
        #查询学生相关课程信息
        sql = "select c.id as id,c.name as name from `stud_course` as s left join course as c on c.id=s.course_id where s.student_id=%s";
        result = databaseOperations.select_many(sql, current_user.id)
        return render_template('student_page.html', student=student, result=result)



#学生课程相关接口
@studentBlue.route('/coruse', methods=['POST', 'GET'])
@login_required
def student_course():
    if request.method == 'GET':
        id = request.args['id']
        #查询本课程的详细信息
        databaseOperations = DatabaseOperations()
        sql = 'select * from course where id=%s'
        course = databaseOperations.select_one(sql, (id))

        #查询这个课程的咨询
        sql = """SELECT * from inform where class_id=%s"""
        informationlst = databaseOperations.select_many(sql, (id))

        return render_template('student_page_related_class.html', course=course,informationlst=informationlst)




#历史签到信息查询
@studentBlue.route('/attend', methods=['POST', 'GET'])
@login_required
def attend():

    if request.method == 'GET':
        id =request.args['id']

        #根据课程id查询当前章节的签到数据
        sql="""SELECT
	s.chapter AS chapter,
	s.is_attendance as is_attendance
	FROM
	`attendance` AS s
	LEFT JOIN stud_course AS c ON c.student_id=s.student_id
WHERE
	c.course_id =%s and c.student_id=%s"""
        databaseOperations = DatabaseOperations()
        attendList=databaseOperations.select_many(sql,(id,current_user.id))

        #查询课程的信息
        sql = 'select * from course where id=%s'
        course = databaseOperations.select_one(sql, (id))

        return render_template( 'student-course-attendance.html',result=attendList,course=course)
