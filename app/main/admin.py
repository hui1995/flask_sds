#!/usr/bin/env python

from flask import render_template, request, session, redirect, Response
# from . import main
from .. import db
from ..models import *
from flask_login import login_required,current_user
from flask import Blueprint
from app import db
adminBlue = Blueprint('admin',__name__)

@adminBlue.route('/index',methods=['POST','GET'])
@login_required
def student_home():
    if request.method == 'GET':




        return render_template('admin_home.html')


# @studentBlue.route('/coruse',methods=['POST','GET'])
# @login_required
# def student_course():
#     if request.method == 'GET':
#         id=request.args['id']
#         course=Course.query.filter(Course.id==id).first()
#
#
#         return render_template('student_page_related_class.html',course=course)
#
# @studentBlue.route('/home',methods=['POST','GET'])
# @login_required
# def home():
#     if request.method == 'GET':
#         student=Student.query.filter(Student.id==current_user.id).first()
#
#
#         return render_template('home.html',student=student)

