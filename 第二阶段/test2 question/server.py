#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ValenW
# @Link    : https://github.com/ValenW
# @Email   : ValenW@qq.com
# @Date    : 2014-12-02 14:10:50
# @Last Modified by:   anchen
# @Last Modified time: 2014-12-04 17:25:17
# TODO:
#   评论与博文是否为空判断

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import time
import re
import tornado.ioloop
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

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
    @tornado.web.authenticated
    def get(self):
        userNames = [u.split(',')[0] for u in\
            open('static/data/userData.txt').readlines()]

        questions = [q.split(';', 3) for q in open("static/data/questionData.txt").readlines()]
        replys = [r.split(';', 3) for r in open("static/data/replyData.txt").readlines()]

        for q in questions:
            print q[2]
        for r in replys:
            print r
            print r[0]

        self.render("index.html", questions=questions, replys=replys)

class LoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            self.render("login_signup.html", reType="login")

    def post(self):
        users = [u.strip() for u in open('static/data/userData.txt').readlines()]
        us = {}
        for i in xrange(len(users)):
            us[users[i].split(',')[0]] = users[i].split(',')[1]

        if self.get_argument("name") in us and\
            us[self.get_argument("name")] == self.get_argument("password"):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.redirect("/login")

class SignupHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            self.render("login_signup.html", reType="signup")

    def post(self):
        name = self.get_argument("name")
        password = self.get_argument("password")

        nameRe = re.compile(r'^\w{6,12}$')
        passRe = re.compile(r'^[A-Z]\w{5,11}$')

        userNames = [u.split(',')[0] for u in\
            open('static/data/userData.txt').readlines()]

        if nameRe.match(name) and passRe.match(password)\
            and not (name in userNames):
            open('static/data/userData.txt', "a+").write(name + ',' + password + '\n')
            self.set_secure_cookie("user", name)
            self.redirect('/')
        else:
            self.redirect('/signup')

class ViewHandler(BaseHandler):
    def get(self, userName, blogName, blogId):
        userNames = [u.split(',')[0] for u in\
            open('static/data/users.txt').readlines()]

        userIn = False
        if userName in userNames:
            if self.get_current_user() == userName:
                userIn = True
        else:
            self.write_error(404)

        blogPath = "static/data/" + blogName + '/blog' + blogId + '.txt'
        commentsPath = "static/data/" + blogName + '/comments' + blogId + '.txt'
        if os.path.exists(blogPath):
            blog = open("static/data/" + blogName + '/blog' + blogId\
                + '.txt').read().split(':', 2)
            comments = [c.split('|', 2 ) for c in open("static/data/" + blogName + '/comments' + blogId\
                + '.txt').readlines()]
        else:
            self.write_error(404)
            return

        self.render("view.html", blog=blog,\
            comments=comments, userIn=userIn, userName=userName, bName=blogName, bId=blogId)

    def post(self, userName, blogName, blogId):
        comment=self.get_argument("comment")
        commentsPath = "static/data/" + blogName + '/comments' + blogId + '.txt'
        open(commentsPath, "a+").write(userName + '|' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '|' + comment + '\n')
        self.redirect("/" + userName + "/" + blogName + "/" + blogId)

class QuestionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("question.html")

    def post(self):
        print "q post"
        title = self.get_argument("title")
        time = self.get_argument("time")
        content = self.get_argument("content")

        if title and time and content:
            name = tornado.escape.xhtml_escape(self.current_user)
            open('static/data/questionData.txt', "a+").write(title + ';' + time + ';' + name + ';' + content + '\n')
            self.redirect('/')
        else:
            self.redirect('/question')

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug": True,
    "cookie_secret": "ETzKXQAGa765YdkL5gEmheJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login"
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/signup", SignupHandler),
    (r"/question", QuestionHandler),
    (r"/logout", LogoutHandler),
    (r".*", BaseHandler)
], **settings)

if __name__ == "__main__":
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
