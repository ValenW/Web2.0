# -*- coding: utf-8 -*-
# @Author  : ValenW
# @Link    : https://github.com/ValenW
# @Email   : ValenW@qq.com
# @Date    : 2015-01-06 14:54:29
# @Last Modified by:   ValenW
# @Last Modified time: 2015-01-06 14:54:29
# TODO:
#   未登录发表预言逻辑错误

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
    creUser = "create table `v_%s` (rediId INT(11) NOT NULL, `atti` INT(11) NOT NULL, UNIQUE KEY `rediId` (`rediId`))"
    insTb = "insert into "
    cotNu = "select * from "
    selTb = "select %s from `%s` where `%s`%s"
    selOr = "select %s from `%s` where %s order by %s limit 0, %s"
    updTb = "update `%s` set `%s`=%d where `%s`=%d"
    delTb = "delete from `%s` where `%s`=%d"
    exiTb = "select table_name from `INFORMATION_SCHEMA`.`TABLES` where table_name ='c_%s' and TABLE_SCHEMA='app_valenw'"
    creComm = "create table `c_%s` (commer VARCHAR(20) NOT NULL, comment TEXT NOT NULL, INDEX (`commer`))"

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
        self.write('error:' + str(status_code) + "<br>当你看见这个页面时，可能是新浪云抽风了，或者新浪云嫌我穷不给我用了。。。<br>攻城狮邮箱：1509563478@qq.com<br>攻城狮支付宝：wwl0816@qq.com<br> 您自个看着办吧。。")

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
        except MySQLdb.Error, e:
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

    def getRedi(self, where="1", sortd="id desc", num=5):
        conn, cur = self.mysql()
        cur.execute(self.selOr % ('*', "redi", where, sortd, num))
        redi = list(cur.fetchall())
        self.closemysql(conn, cur)
        timenow = datetime.datetime.now()
        votes = self.getVote() if self.get_current_user() else {}
        for i in xrange(len(redi)):
            redi[i] = list(redi[i])
            redi[i].append(str(-(timenow - redi[i][2]).days))
            redi[i][2] = redi[i][2].strftime("%Y-%m-%d %H:%M:%S")

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
        return redi

    def getVote(self):
        conn, cur = self.mysql()
        cur.execute(self.cotNu + "v_" + self.userName())
        re =  dict(list(cur.fetchall()))
        self.closemysql(conn, cur)
        return re

    def addUser(self, name, pasw):
        conn, cur = self.mysql()
        cur.execute(self.insTb + "users(name, password) values(%s, %s)", (name, pasw))
        cur.execute(self.creUser % name)
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
            cur.execute(self.selTb % ("`down`", "redi", "id", "=%d" % (rediId)))
            oldDown = cur.fetchone()[0]
            newDown = oldDown + 1 if atti == 1 else oldDown - 1
            cur.execute(self.updTb % ("redi", "down", newDown, "id", rediId))
        else:
            cur.execute(self.selTb % ("`up`", "redi", "id", "=%d" % (rediId)))
            oldUp = cur.fetchone()[0]
            newUp = oldUp + 1 if atti == 0 else oldUp - 1
            cur.execute(self.updTb % ("redi", "up", newUp, "id", rediId))
        conn.commit()
        if close:
            self.closemysql(conn, cur)
        return

    def toVote(self, rediId, atti):
        #atti: 0 for up, 1 for down
        conn, cur = self.mysql()
        cur.execute(self.selTb % ("`atti`", "v_" + self.userName(), "rediId", "=%d" % (rediId)))
        vo = cur.fetchone()
        self.rediUpdate(rediId, atti, conn, cur)
        if type(vo) != type(None):
            cur.execute(self.updTb % ("v_" + self.userName(), "atti", atti, "rediId", rediId))
            self.rediUpdate(rediId, 3-atti, conn, cur)
        else:            cur.execute(self.insTb + "v_" + self.userName() + "(rediId, atti) values(%s, %s)", (rediId, atti))
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

    def getComm(self, rediId):
        conn, cur = self.mysql()
        cur.execute(self.exiTb % rediId)
        if len(cur.fetchall()) > 0:
            cur.execute(self.cotNu + "`c_%s`" % rediId)
            com = cur.fetchall()[::-1]
        else:
            com = "None"
        self.closemysql(conn, cur)
        print com
        return com

    def addComm(self, rediId, comm):
        conn, cur = self.mysql()
        cur.execute(self.exiTb % rediId)
        if len(cur.fetchall()) <= 0:
            cur.execute(self.creComm % (rediId))
            conn.commit()
        cur.execute(self.insTb + "`c_%s`(`commer`, `comment`) values('%s', '%s')" % (rediId, self.userName(), comm))
        self.closemysql(conn, cur)
        return

class MainHandler(BaseHandler):
    def get(self):
        key = self.get_argument("key", "None")
        if key == "None":
            redi = self.getRedi()
        elif key == "hot":
            redi = self.getRedi("1", "up + down desc")
        else:
            redi = self.getRedi("1", key + " desc")
        self.render("index.html", redi=redi, userName=self.userName())

class LoginHandler(BaseHandler):
    def post(self):
        if self.get_current_user():
            self.write('-1')
            return

        name = self.get_argument("name").encode('utf8')
        password = self.get_argument("password").encode('utf8')

        us = self.getUsers()

        print us
        print name
        print password
        print "in" if name in us else "not in"
        
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
        if op == 'r':
            self.toReles(rediId, atti)
        else:
            self.toVote(rediId, atti)
        self.write('1')

class SignupHandler(BaseHandler):
    def post(self):
        if self.get_current_user():
            self.write('-1')
            return

        name = self.get_argument("name").encode('utf8')
        password = self.get_argument("password").encode('utf8')

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
        self.render('redi.html', userName=self.userName())

    def post(self):
        name = self.get_argument("name")
        content = self.get_argument("content")
        time = datetime.datetime.strptime(self.get_argument("time"), "%m/%d/%Y %H:%M %p")

        conn, cur = self.mysql()
        n = cur.execute(self.cotNu + "redi")
        cur.execute(self.insTb + "redi(id, auth, time, content, up, down, tauth) values(%s, %s, %s, %s, %s, %s, %s)", (n+1, name, time, content, 0, 0, self.userName()))
        self.write("1")

class LoadHandler(BaseHandler):
    def get(self, stype, fromId):
        if stype == "hot":
            redi = self.getRedi('up + down' + '<' + fromId, "up + down desc")
        else:
            redi = self.getRedi(stype + '<' + fromId, stype + " desc")
        self.write(tornado.escape.json_encode( redi ))

class CommentHandler(BaseHandler):
    def get(self, rediId):
        redi = self.getRedi("`id`=%s" % (rediId))[0]
        comment = self.getComm(rediId)
        self.render("comment.html", r=redi, comment=comment, userName=self.userName())

    def post(self, rediId):
        comm = self.get_argument("comment")
        self.addComm(rediId, comm)
        redi = self.getRedi("`id`=%s" % (rediId))[0]
        comment = self.getComm(rediId)
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
    (r"/signup", SignupHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/redi", RediHandler),
    (r"/vote", VoteHandler),
    (r"/load/(\w+)/(\d+)", LoadHandler),
    (r"/com/(\d+)", CommentHandler),
    (r".*", BaseHandler)
], **settings)

application = sae.create_wsgi_app(app)
