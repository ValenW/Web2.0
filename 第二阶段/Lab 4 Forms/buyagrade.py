#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-20 20:56:19
# @Author  : ValenW (ValenW@qq.com)
# @Link    : https://github.com/ValenW

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import re
import tornado.ioloop
import tornado.web

class user:
    def __init__(self, name, section, cardId, cardType):
        self.name = name
        self.section = section
        self.cardId = cardId
        self.cardType = cardType

class PostHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name", "None").strip()
        section = self.get_argument("section", "None").strip()
        cardId = self.get_argument("cardId", "None").strip()
        cardType = self.get_argument("cardType", "None").strip()

        if name == "None" or section == "None" or cardId == "None" or cardType == "None":
            reType = 'notCompleted'
        elif (cardType == 'Visa' and cardId[0] != '4')\
            or (cardType == 'Mastercard' and cardId[0] != '5'):
            reType = 'notValid'
        else:
            pattern = re.compile(r'^(\d{4}([- ]?))(\d{4}\2){2}(\d){4}$')
            if not pattern.match(cardId):
                reType = 'notValid'
            else:
                cardId = cardId.replace(" ", "").replace("-", "")
                sum = 0
                for i in xrange(16):
                    if i % 2 == 1:
                        sum += int(cardId[i])
                        print cardId[i]
                    elif int(cardId[i])*2 < 10:
                        sum += int(cardId[i])*2
                        print int(cardId[i])*2
                    else:
                        sum += (int(cardId[i])*2 % 10) + 1
                print sum
                if sum % 10 != 0:
                    reType = "notValid"
                else:
                    reType = "valid"

        if reType == 'notCompleted':
            self.render('failed.html', reType='notCompleted')
        elif reType == 'notValid':
            self.render('failed.html', reType='notValid')
        else:
            inf = open('static/suckers.txt', 'a+')
            inf.write(name + ';' + section + ';' + cardId + ';' + cardType + '\n')
            inf.close()
            inf = open('static/suckers.txt', 'r')
            infs = inf.read()
            self.render('succed.html', infs=infs, user=user(name, section, cardId, cardType))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('buyagrade.html')

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/post", PostHandler)
], debug=True, **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
