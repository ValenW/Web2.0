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

from sae.ext.storage import monkey
monkey.patch_all()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        else:
            self.write('error:' + str(status_code))

class MainHandler(BaseHandler):
    def get(self):
        votes = {}
        userName = "None"
        if self.get_current_user():
            userName = tornado.escape.xhtml_escape(self.current_user)
            votePath = "/s/data/v_" + userName
            if os.path.exists(votePath):
                print votePath
                tvotes = [v.split(',', 1) for v in open(votePath).read().strip().split('\n')]
                for i in xrange(len(tvotes)):
                    votes[tvotes[i][0]] = int(tvotes[i][1])

        redi = [r.split(';', 5) for r in open("/s/data/redi").read().strip().split('\n')]
        redi = redi[::-1]

        timenow = datetime.datetime.now()
        for r in redi:
            r.append(-(timenow - datetime.datetime.strptime(r[2],"%Y-%m-%d %H:%M:%S")).days)
            if r[4] >= r[5]:
                r.append(' voted')
                r.append('')
            else:
                r.append('')
                r.append(' voted')
            if self.get_current_user() and r[0] in votes:
                if votes[r[0]] == 1:
                    r[7] = r[7] + ' btn-info'
                    r[8] = r[8] + ' btn-default'
                else:
                    r[7] = r[7] + ' btn-default'
                    r[8] = r[8] + ' btn-info'
            else:
                r[7] = r[7] + ' btn-default'
                r[8] = r[8] + ' btn-default'

        self.render("index.html", redi=redi, userName=userName)

class LoginHandler(BaseHandler):
    def post(self):
        if self.get_current_user():
            self.write('-1')
            return

        name = self.get_argument("name")
        password = self.get_argument("password")

        users = [u.strip() for u in open(os.path.join(os.path.dirname(__file__), "/s/data/users")).read().strip().split('\n')]
        us = {}
        print users
        for i in xrange(len(users)):
            us[users[i].split(';')[0]] = users[i].split(';')[1]

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

        userName = tornado.escape.xhtml_escape(self.current_user)
        votePath = "/s/data/v_" + userName
        votes = {}
        if os.path.exists(votePath):
            tvotes = [v.split(',', 1) for v in open(votePath).read().strip().split('\n')]
            for i in xrange(len(tvotes)):
                votes[int(tvotes[i][0])] = int(tvotes[i][1])
        else:
            open(votePath, 'w')

        redi = [r.split(';', 5) for r in open("/s/data/redi").read().strip().split('\n')]

        s = ""
        if op == 'r':
            if rid > 0:
                votes.pop(rid)
                for r in redi:
                    if int(r[0]) == rid:
                        r[4] = str(int(r[4]) - 1)
                    s = s + ";".join(r).strip() + '\n'
            else:
                votes.pop(-rid)
                for r in redi:
                    if int(r[0]) == -rid:
                        r[5] = str(int(r[5]) - 1)
                    s = s + ";".join(r).strip() + '\n'
        elif rid in votes or -rid in votes:
            if rid > 0:
                votes[rid] = 1;
                for r in redi:
                    if int(r[0]) == rid:
                        r[4] = str(int(r[4]) + 1)
                        r[5] = str(int(r[5]) - 1)
                    s = s + ";".join(r).strip() + '\n'
            else:
                votes[-rid] = -1
                for r in redi:
                    if int(r[0]) == -rid:
                        r[4] = str(int(r[4]) - 1)
                        r[5] = str(int(r[5]) + 1)
                    s = s + ";".join(r).strip() + '\n'
        else:
            if rid > 0:
                votes[rid] = 1
                for r in redi:
                    if int(r[0]) == rid:
                        r[4] = str(int(r[4]) + 1)
                    s = s + ";".join(r).strip() + '\n'
            else:
                votes[-rid] = -1
                for r in redi:
                    if int(r[0]) == -rid:
                        r[5] = str(int(r[5]) + 1)
                    s = s + ";".join(r).strip() + '\n'

        open("/s/data/redi", 'w').write(s)

        v0 = tuple(votes)
        v1 = tuple(votes.values())
        s = ""
        for i in xrange(len(v0)):
            s = s + str(v0[i]) + ',' + str(v1[i]) + '\n'
        open(votePath, 'w').write(s)

        self.write('1')

class SignupHandler(BaseHandler):
    def post(self):
        if self.get_current_user():
            self.write('-1')
            return

        name = self.get_argument("name")
        password = self.get_argument("password")

        users = [u.strip() for u in open(os.path.join(os.path.dirname(__file__), "/s/data/users")).read().strip().split('\n')]
        us = {}
        for i in xrange(len(users)):
            us[users[i].split(';')[0]] = users[i].split(';')[1]

        if name in us:
            self.write("0")
            return
        else:
            s = open(os.path.join(os.path.dirname(__file__), "/s/data/users")).read()
            s = s + '\n' + str(name) + ';' + str(password)
            open(os.path.join(os.path.dirname(__file__), "/s/data/users"), 'w').write(s)
            self.set_secure_cookie("user", name)
            self.write("1")

class RediHandler(BaseHandler):
    def get(self):
        self.render('redi.html')

    def post(self):
        
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
