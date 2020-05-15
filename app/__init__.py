
from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
pymysql.install_as_MySQLdb()
db = SQLAlchemy()
from flask_login import LoginManager


from app.models import Student,Teacher,Admin
from flask import session,request
def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:breathcoder.com@148.70.172.191:3306/sds'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = 'INPUT A STRING'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login_views'

    @login_manager.user_loader
    def load_user(userid):
        type=session.get("type")
        if type==1 and  "student" in request.url:#s说明是学生

            return Student.query.get(userid)
        elif type==2 and "teacher" in request.url:
            return Teacher.query.get(userid)
        elif type==3 and 'admin' in request.url:
            print("----------")
            admin=Admin()
            return admin

    db.init_app(app)

    from .main import mainBlu as main_blueprint
    from .main import teacherBlu as teacherBlu
    from .main import studentBlue as studentBlue
    from .main import adminBlue as adminBlue
    app.register_blueprint(main_blueprint)
    app.register_blueprint(teacherBlu,url_prefix='/teacher')
    app.register_blueprint(studentBlue,url_prefix='/student')
    app.register_blueprint(adminBlue,url_prefix='/admin')

    return app





