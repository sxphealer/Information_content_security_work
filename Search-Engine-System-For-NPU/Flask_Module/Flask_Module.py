#! /usr/bin/env python
#coding=utf-8
from __future__ import unicode_literals
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
sys.path.append("../")
from Whoosh_Module.Whoosh_Module import Whoosh_Module
from flask import Flask,url_for,render_template,request

Whoosh = None
flask_app = Flask(__name__)
@flask_app.route('/',methods=['GET', 'POST'])
def index():
    global Whoosh
    if request.method == 'POST':
        keyword=request.form['keyword']
        results = Whoosh.search(keyword)
        return render_template('result.html',results=results,keyword=keyword)
    else :
        return render_template('index.html',results=None)


class Flask_Module(object):
    def __init__(self,WhooshName):
        global Whoosh
        Whoosh = WhooshName
    def run(self):
        #flask_app.debug=True
        flask_app.run(host='0.0.0.0')

if __name__ == '__main__':
    Whoosh=Whoosh_Module()
    #flask_app.debug=True
    flask_app.run(host='0.0.0.0')

