
from flask import Flask
from flask_login import LoginManager
from app.DatabaseOperations import *


from app.models import User
from flask import session,request
#配置文件
def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True

    app.config['SECRET_KEY'] = 'INPUT A STRING'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login_views'


    #权限保护，每次访问接口，都需要访问这个接口
    @login_manager.user_loader
    def load_user(userid):

        type=session.get('user_type')
        userid=userid.replace("(","")
        userid=userid.replace(")","")
        userid=userid.replace("'","")
        userid=userid.replace(",","")
        #如果用户类型为1，则进行以下操作
        if type==1 and  "student" in request.url:#s说明是学生
            #查询数据库，并把用户返回
            databaseOperations = DatabaseOperations()
            sql = "select id,name,password from student where id=%s"
            row=databaseOperations.select_one(sql,userid)
            if row is not None:
                user =User(row[0],row[1],row[2])
                return user
        elif type==2 and "teacher" in request.url:
            databaseOperations = DatabaseOperations()
            sql = "select id,name,password from teacher where id=%s"
            row = databaseOperations.select_one(sql, (userid))
            if row is not None:
                user = User(row[0], row[1], row[2])
                return user
        elif type==3 and 'admin' in request.url:
            user=User(0,'admin','admin')
            return user

    #注册蓝图
    from .main import mainBlu as main_blueprint
    from .main import teacherBlu as teacherBlu
    from .main import studentBlue as studentBlue
    from .main import adminBlue as adminBlue
    app.register_blueprint(main_blueprint)
    app.register_blueprint(teacherBlu,url_prefix='/teacher')
    app.register_blueprint(studentBlue,url_prefix='/student')
    app.register_blueprint(adminBlue,url_prefix='/admin')

    return app





