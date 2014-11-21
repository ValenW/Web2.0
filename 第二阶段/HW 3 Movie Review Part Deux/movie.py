#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ValenW
# @Date:   2014-11-14 19:02:31
# @Last Modified by:   ValenW
# @Last Modified time: 2014-11-17 00:58:40

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import glob

class theFime:
    def __init__(self, name, proYear, score, comNum, overvPngPath):
        self.name = name
        self.proYear = proYear
        self.score = score
        self.comNum = comNum
        self.overvPngPath = overvPngPath

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        fime = self.get_argument('film', 'tmnt')
        filePath = os.path.join(os.path.dirname(__file__),\
            "static/movies/" + fime)
        # filePatht = os.path.join(filePath, "movies")
        # filePath = os.path.join(filePatht, fime)

        infFile = open(os.path.join(filePath, "info.txt")).readlines()
        fimeName = infFile[0].strip()
        productionYear = infFile[1].strip()
        score = infFile[2].strip()
        comNum = infFile[3].strip()
        overvPngPath = os.path.join(r"static/movies/",\
            fime + "/generaloverview.png")
        refime = theFime(fimeName, productionYear, score, comNum, overvPngPath)

        overvPngPath = os.path.join(filePath, "generaloverview.png")

        overviewFile = open(os.path.join(filePath, "generaloverview.txt"))
        informs = overviewFile.read().splitlines()
        infdict = []
        for inform in informs:
            infdict.append([inform.split(':')[0], inform.split(':')[1]])
            # print infdict[-1]

        reviewFiles = glob.glob(filePath + r'/review*.txt')
        # print(reviewFiles)
        revs = []
        for reviewFile in reviewFiles:
            revs.append([item for item in open(reviewFile).read().splitlines()])

        self.render('movie.html', theFime=refime, infdict=infdict, revs=revs)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates")
}

application = tornado.web.Application([
    (r"/?film=(\w*)", MainHandler),
    (r"/", MainHandler)
], debug=True, **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
