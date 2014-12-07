#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ValenW
# @Link    : https://github.com/ValenW
# @Email   : ValenW@qq.com
# @Date    : 2014-11-29 09:17:00
# @Last Modified by:   ValenW
# @Last Modified time: 2014-12-02 09:30:41

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import re
import string
import tornado.ioloop
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class user:
    def __init__(self, name, sex, age, perType, OS, forSex, forAge):
        self.name = name
        self.sex = sex
        self.age = age
        self.perType = perType
        self.OS = OS
        self.forSex = forSex
        self.forAge = forAge

class MainHandler(tornado.web.RequestHandler):
    """docstring for MainHandler"""
    def get(self):
        self.render("index.html")

    def post(self):
        reType = None
        name = self.get_argument('name', None)
        sex = self.get_argument('sex', None)
        age = self.get_argument('age', None)
        perType = self.get_argument('perType', None)
        OS = self.get_argument('OS', None)
        forSex = self.get_arguments('forSex', None)
        forAge = self.get_arguments('forAge', None)

        if not name or not sex or not OS or not perType or forSex == [] or forAge == []:
            self.render("failed.html", reType="notCompleted")
            return

        users = []
        for i in open("static/singles.txt", 'r').read().splitlines():
            users.append([ii for ii in i.split(',')])

        for user in users:
            if user[0] == name:
                self.render("failed.html", reType="unvalidName")
                return

        ageRe = re.compile(r'^([1-9]\d?)|0$')
        perTypeRe = re.compile(r'^[IE][NS][FT][JP]$')
        if not ageRe.match(age) or not ageRe.match(forAge[0])\
            or not ageRe.match(forAge[1]) or not perTypeRe.match(perType)\
            or int(forAge[0]) >= int(forAge[1]):
            self.render("failed.html", reType="unValid")
            return

        if self.request.files:
            files = self.request.files['picture']
            for pic in files:
                print pic['filename'].split('.')[-1]
                if pic['filename'].split('.')[-1] != 'jpg':
                    self.render("failed.html", reType="unValid")
                    return
                filename = name.lower().replace(' ', '_') + ".jpg"
                f = open("static/images/" + filename, "wb")
                f.write(pic["body"])
                f.close()
        
        if forSex == ['M', 'F']:
            forSex = 'MF'
        elif forSex == ['M']:
            forSex = 'M'
        else:
            forSex = 'F'
        writeF = open("static/singles.txt", 'a+')
        writeF.write(name + ',' + sex + ',' + age + ',' + perType + ','\
            + OS + ',' + forSex + ',' + forAge[0] + ',' + forAge[1] + '\n')
        writeF.close()

        forAge[0] = int(forAge[0])
        forAge[1] = int(forAge[1])
        age = int(age)

        reUsers = []
        for user in users:
            user[6] = int(user[6])
            user[7] = int(user[7])
            if (user[1] == forSex or forSex == 'MF')\
                and (user[5] == sex or user[5] == 'MF'):
                user.append(0)
                reUsers.append(user)

        for ru in reUsers:
            if (age >= ru[6] and age <= ru[7])\
                and (int(ru[2]) >= forAge[0] and int(ru[2]) <= forAge[1]):
                ru[8] = ru[8] + 1
            if ru[4] == OS:
                ru[8] = ru[8] + 2
            for i in xrange(4):
                if ru[3][i] == perType[i]:
                    ru[8] = ru[8] + 1

        mUsers = [u for u in reUsers if u[8] >= 3]
        for u in mUsers:
            if os.path.exists("static/images/" + u[0].lower().replace(' ', '_') + ".jpg"):
                u.append(True)
            else:
                u.append(False)
        mUsers.sort(key=lambda x: (x[8]), reverse=True)
        self.render("results.html", uName=name, users=mUsers)

class LoginHandler(tornado.web.RequestHandler):
    """docstring for LoginHandler"""
    def get(self):
        name=self.get_argument('username')
        users = []
        for i in open("static/singles.txt", 'r').read().splitlines():
            users.append([ii for ii in i.split(',')])

        userId = -1
        for user in users:
            userId = userId + 1
            if user[0] == name:
                break
        if userId == -1:
            self.render("failed.html", reType=notValid)
            return
        else:
            sex = users[userId][1]
            age = int(users[userId][2])
            perType = users[userId][3]
            OS = users[userId][4]
            forSex = users[userId][5]
            forAge = [int(users[userId][6]), int(users[userId][7])]
            users.pop(userId)
        reUsers = []
        for user in users:
            user[6] = int(user[6])
            user[7] = int(user[7])
            if (user[1] == forSex or forSex == 'MF')\
                and (user[5] == sex or user[5] == 'MF'):
                user.append(0)
                reUsers.append(user)

        for ru in reUsers:
            if (age >= ru[6] and age <= ru[7])\
                and (int(ru[2]) >= forAge[0] and int(ru[2]) <= forAge[1]):
                ru[8] = ru[8] + 1
            if ru[4] == OS:
                ru[8] = ru[8] + 2
            for i in xrange(4):
                if ru[3][i] == perType[i]:
                    ru[8] = ru[8] + 1

        mUsers = [u for u in reUsers if u[8] >= 3]
        for u in mUsers:
            if os.path.exists("static/images/" + u[0].lower().replace(' ', '_') + ".jpg"):
                u.append(True)
            else:
                u.append(False)
        mUsers.sort(key=lambda x: (x[8]), reverse=True)
        self.render("results.html", uName=name, users=mUsers)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler)
], debug=True, **settings)

if __name__ == "__main__":
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
