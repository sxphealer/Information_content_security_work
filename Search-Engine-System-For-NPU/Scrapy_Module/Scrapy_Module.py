#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.split(os.path.realpath(__file__))[0])
from Scrapy_Project.spiders.Scrapy_ModuleSpider import Scrapy_ModuleSpider
# scrapy api
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
import  scrapy.utils.project as Scr_pro
import os
class Scrapy_Module(object):
    Scrapy_Module_setting = None
    def __init__(self):
        #记录当前工作用于还原工作目录
        cwd = os.getcwd()
        #获取当前文件所在目录，并把工作目录切换到文件所在目录，用于读取Scrapy项目settings
        file_dir = os.path.split(os.path.realpath(__file__))[0]
        os.chdir(file_dir)
        print cwd
        print os.getcwd()
        self.Scrapy_Module_setting = Scr_pro.get_project_settings()
        #关闭打印信息
        self.Scrapy_Module_setting.set('LOG_ENABLED',False)
        log.start(logfile='Scrapy_Module.log',loglevel=log.DEBUG,logstdout=False)
        #将工作目录还原为之前的工作目录
        os.chdir(cwd)
    def spider_closing(self,spider):
        #收到Spider结束信号后关闭reactor
        log.msg("Closing reactor", level=log.INFO)
        reactor.stop()
    def crawl(self):
        spider = Scrapy_ModuleSpider()
        Runner = CrawlerRunner(self.Scrapy_Module_setting)
        cra = Runner.crawl(spider)
        # stop reactor when spider closes
        cra.addBoth(lambda _: self.spider_closing(cra))
        log.msg("Run reactor", level=log.INFO)
        reactor.run()
    def run(self):
        while True:
            self.crawl()


if __name__ == '__main__' :
    Scrapy_Module().run()
