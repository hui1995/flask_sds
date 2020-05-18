#!/usr/bin/env python


import pymysql
pymysql.install_as_MySQLdb()

#s链接数据
class DatabaseOperations:
    __db_url = '148.70.172.191'
    __db_username = 'root'
    __db_password = 'breathcoder.com'
    __db_name = 'sds'
    __db_port = 3306
    __db = None

    def __init__(self):
        self.__db = self.db_connect()

    def __del_(self):
        self.__db.close()

    def db_connect(self):
        self.__db = pymysql.connect(self.__db_url, self.__db_username,
                                    self.__db_password, self.__db_name,
                                    self.__db_port,charset='utf8')
        return self.__db



    def select_one(self,sql,args):
        cur=self.__db.cursor()
        cur.execute(sql,args)
        row=cur.fetchone()

        cur.close()
        return row

    def select_many(self,sql,args):
        cur=self.__db.cursor()
        cur.execute(sql,args)
        rows=cur.fetchall()

        cur.close()
        return rows
    def insert_one(self,sql,args):
        cur=self.__db.cursor()

        cur.execute(sql,args)
        self.__db.commit()
        cur.close()

    def update(self,sql,args):
        cur=self.__db.cursor()


        cur.execute(sql,args)
        self.__db.commit()
        cur.close()

    def delete(self, sql, args):
        cur = self.__db.cursor()

        cur.execute(sql, args)
        self.__db.commit()
        cur.close()