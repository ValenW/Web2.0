# -*- coding: utf-8 -*-
# @Author  : ValenW
# @Link    : https://github.com/ValenW
# @Email   : ValenW@qq.com
# @Date    : 2015-01-06 14:54:29
# @Last Modified by:   ValenW
# @Last Modified time: 2015-01-06 14:54:29

import os
import time
import datetime
import tornado.wsgi
import sae
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BaseHandler(tornado.web.RequestHandler):
    creTb = "create table "
    insTb = "insert into "
    cotNu = "select * from "
    selTb = "select `%s` from `%s` where `%s`=%d"
    updTb = "update `%s` set `%s`=%d where `%s`=%d"
    delTb = "delete from `%s` where `%s`=%d"

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def userName(self):
        if self.get_current_user():
            return tornado.escape.xhtml_escape(self.current_user)
        else:
            return "None"

    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        else:
            self.write('error:' + str(status_code))

    def mysql(self):
        try:
            conn = MySQLdb.connect(
                host=sae.const.MYSQL_HOST,
                user=sae.const.MYSQL_USER,
                passwd=sae.const.MYSQL_PASS,
                db=sae.const.MYSQL_DB,
                port=int(sae.const.MYSQL_PORT),
                charset='utf8')
            cur = conn.cursor()
            return conn, cur
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return NULL, NULL

    def closemysql(self, conn, cur):
        conn.commit()
        cur.close()
        conn.close()

    def getUsers(self):
        conn, cur = self.mysql()
        cur.execute(self.cotNu + "users")
        re =  dict(list(cur.fetchall()))
        self.closemysql(conn, cur)
        return re

    def getRedi(self, num=10):
        conn, cur = self.mysql()
        cur.execute(self.cotNu + "redi")
        re =  list(cur.fetchmany(num)[::-1])
        self.closemysql(conn, cur)
        return re

    def getVote(self):
        conn, cur = self.mysql()
        cur.execute(self.cotNu + "v_" + self.userName())
        re =  dict(list(cur.fetchall()))
        self.closemysql(conn, cur)
        return re

    def addUser(self, name, pasw):
        conn, cur = self.mysql()
        cur.execute(self.insTb + "users(name, password) values(%s, %s)", (name, pasw))
        cur.execute(self.creTb + "v_" + name + "(rediId INT(11) NOT NULL, atti INT(11) NOT NULL, UNIQUE KEY rediId (rediId))")
        conn.commit()
        self.closemysql(conn, cur)
        return

    def rediUpdate(self, rediId, atti, conn="None", cur="None"):
        #atti: 0 for up + 1
        #        1 for down + 1
        #        2 for up - 1
        #        3 for down - 1
        close = False
        if conn == "None":
            conn, cur = self.mysql()
            close = True
        if atti % 2:
            cur.execute(self.selTb % ("down", "redi", "id", rediId))
            oldDown = cur.fetchone()[0]
            newDown = oldDown + 1 if atti == 1 else oldDown - 1
            print "atti=%d oldDown=%d newDown=%d" % (atti, oldDown, newDown)
            cur.execute(self.updTb % ("redi", "down", newDown, "id", rediId))
        else:
            cur.execute(self.selTb % ("up", "redi", "id", rediId))
            oldUp = cur.fetchone()[0]
            newUp = oldUp + 1 if atti == 0 else oldUp - 1
            print "atti=%d oldUp=%d newUp=%d" % (atti, oldUp, newUp)
            cur.execute(self.updTb % ("redi", "up", newUp, "id", rediId))
        conn.commit()
        if close:
            self.closemysql(conn, cur)
        return

    def toVote(self, rediId, atti):
        #atti: 0 for up, 1 for down
        conn, cur = self.mysql()
        cur.execute(self.selTb % ("atti", "v_" + self.userName(), "rediId", rediId))
        vo = cur.fetchone()
        self.rediUpdate(rediId, atti, conn, cur)
        if type(vo) != type(None):
            print "vo != None"
            cur.execute(self.updTb % ("v_" + self.userName(), "atti", atti, "rediId", rediId))
            self.rediUpdate(rediId, 3-atti, conn, cur)
        else:
            print "vo == None"
            cur.execute(self.insTb + "v_" + self.userName() + "(rediId, atti) values(%s, %s)", (rediId, atti))
        conn.commit()
        self.closemysql(conn, cur)
        return

    def toReles(self, rediId, atti):
        conn, cur = self.mysql()
        cur.execute(self.delTb % ("v_" + self.userName(), "rediId", rediId))
        self.rediUpdate(rediId, atti+2, conn, cur)
        conn.commit()
        self.closemysql(conn, cur)
        return

class MainHandler(BaseHandler):
    def get(self):
        votes = self.getVote() if self.get_current_user() else {}

        redi = self.getRedi()
        timenow = datetime.datetime.now()
        for i in xrange(len(redi)):
            redi[i] = list(redi[i])
            redi[i].append(-(timenow - redi[i][2]).days)

            if redi[i][4] >= redi[i][5]:
                redi[i].append(' voted')
                redi[i].append('')
            else:
                redi[i].append('')
                redi[i].append(' voted')
            if self.get_current_user() and redi[i][0] in votes:
                if votes[redi[i][0]] == 0:
                    redi[i][8] = redi[i][8] + ' btn-info'
                    redi[i][9] = redi[i][9] + ' btn-default'
                else:
                    redi[i][8] = redi[i][8] + ' btn-default'
                    redi[i][9] = redi[i][9] + ' btn-info'
            else:
                redi[i][8] = redi[i][8] + ' btn-default'
                redi[i][9] = redi[i][9] + ' btn-default'

        self.render("index.html", redi=redi, userName=self.userName())

class LoginHandler(BaseHandler):
    def post(self):
        if self.get_current_user():
            self.write('-1')
            return

        name = self.get_argument("name")
        password = self.get_argument("password")

        us = self.getUsers()

        if name in us and us[name] == password:
            self.set_secure_cookie("user", name)
            self.write("1")
        else:
            self.write("0")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class VoteHandler(BaseHandler):
    def post(self):
        rid = int(self.get_argument("id"))
        op = self.get_argument("o")
        rediId = rid if rid > 0 else -rid
        atti = 0 if rid > 0 else 1

        print "rid=%s id=%s atti=%s" %(rid, rediId, atti)

        if op == 'r':
            print "toReles"
            self.toReles(rediId, atti)
        else:
            self.toVote(rediId, atti)
            print "toVote"
        self.write('1')

class SignupHandler(BaseHandler):
    def post(self):
        if self.get_current_user():
            self.write('-1')
            return

        name = self.get_argument("name")
        password = self.get_argument("password")

        us = self.getUsers()

        if name in us:
            self.write("0")
            return
        else:
            self.addUser(name, password)
            self.set_secure_cookie("user", name)
            self.write("1")

class RediHandler(BaseHandler):
    def get(self):
        self.render('redi.html')

    def post(self):
        name = self.get_argument("name")
        content = self.get_argument("content")
        time = datetime.datetime.strptime(self.get_argument("time"), "%m/%d/%Y %H:%M %p")

        conn, cur = self.mysql()
        n = cur.execute(self.cotNu + "redi")
        cur.execute(self.insTb + "redi(id, auth, time, content, up, down, tauth) values(%s, %s, %s, %s, %s, %s, %s)", (n+1, name, time, content, 0, 0, self.userName()))
        self.write("1")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "/static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug": True,
    "cookie_secret": "ETzKXQAGa765YdkL5gEmheJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login"
}

app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/vote", VoteHandler),
    (r"/signup", SignupHandler),
    (r"/logout", LogoutHandler),
    (r"/redi", RediHandler),
    (r".*", BaseHandler)
], **settings)

application = sae.create_wsgi_app(app)
