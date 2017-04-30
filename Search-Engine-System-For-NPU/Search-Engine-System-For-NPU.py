#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from Scrapy_Module.Scrapy_Module import Scrapy_Module
from Whoosh_Module.Whoosh_Module import Whoosh_Module
from Flask_Module.Flask_Module import Flask_Module

__author__ = "Higor"
__team__ = "Team of IS"
__version__ = "v1.0"

class Search_Engine_System_For_NPU(object):
    def __init__(self):
        Scrapy = Scrapy_Module()
        Whoosh = Whoosh_Module()
        self.Flask = Flask_Module(Whoosh)
        self.Scrapytask = threading.Thread(target=Scrapy.run)
        self.Whooshtask = threading.Thread(target=Whoosh.run)
    def run(self):
        self.Scrapytask.start()
        self.Whooshtask.start()
        self.Flask.run()
        self.Scrapytask.join()
        self.Whooshtask.join()

if __name__ == '__main__':
     Search_Engine_System_For_NPU().run()

