
from flask_login import UserMixin

#用户实体类

class User( UserMixin):
    id=None
    name=None
    password=None

    def __init__(self,id,name,password):
        self.id=id,
        self.name=name,
        self.password=password
















