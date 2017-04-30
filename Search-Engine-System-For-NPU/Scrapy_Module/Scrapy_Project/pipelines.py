# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy import log
class Scrapy_ModulePipeline(object):
    filename=0
    lastnamefileName=None
    lastnamefile=None
    def __init__(self):
        file_dir = os.path.split(os.path.realpath(__file__))[0]
        self.resultdir = file_dir+'/source/'
        self.lastnamefileName = file_dir+'/filename'
        if not os.path.exists(self.resultdir):
            os.mkdir(self.resultdir)
        if os.path.isfile(self.lastnamefileName):
            self.lastnamefile = open(self.lastnamefileName,'r')
            self.filename = int(self.lastnamefile.readline())
            self.lastnamefile.close()
        else:
            self.lastnamefile = open(self.lastnamefileName,'w')
            self.lastnamefile.write(str(self.filename))
            self.lastnamefile.close()

    def process_item(self, item, spider):
        if 'content' not in item :
            return item
        if len(item['content'])>5 :
            self.filename=self.filename+1
            #print self.filename
            try:
                self.resultfile = open(self.resultdir.encode('utf-8')+str(self.filename).encode('utf-8'),'w+')
                self.resultfile.write(str(item['cururl'].encode('utf-8')))
                self.resultfile.write("\n")
                for text in item['title']:
                    title = text.encode('utf-8')
                    self.resultfile.write(str(title))
                    self.resultfile.write("\n")
                content = item['content'].encode('utf-8')
                #去除空行，不然文件内会有很多空行
                content='\n'.join(content.split())
                self.resultfile.write(content)
                self.resultfile.write("\n")
                self.resultfile.close()
            except Exception,e:
                log.msg("Write result file failed.", level=log.ERROR)
                log.msg(e, level=log.ERROR)
            try:
                self.lastnamefile = open(self.lastnamefileName,'w')
                self.lastnamefile.write(str(self.filename))
                self.lastnamefile.close()
            except Exception,e:
                log.msg("Write lastnamefileName file failed.", level=log.ERROR)
                log.msg(e, level=log.ERROR)
        return item
