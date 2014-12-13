#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ValenW
# @Link    : https://github.com/ValenW
# @Email   : ValenW@qq.com
# @Date    : 2014-12-13 16:40:54
# @Last Modified by:   ValenW
# @Last Modified time: 2014-12-13 22:17:59

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import re

inf = file("in.html", 'r')
outf = file("out.html", 'w')
admi = inf.readlines()

fre = re.compile(r'fcontent[\d+]=')

for a in admi:
    i = a.find('=')
    a = a[i+1:-2]
    a = a.replace('<br>', '\\n\\\n')
    a = fre.sub('', a) + r' + "=====\n" + ' + '\n'
    print a
    outf.write(a)
