# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../Scrapy_Module/")#Flask_Module Entry
sys.path.append("Scrapy_Module/")#Search-Engine-System-For-NPU Entry
from Scrapy_Project.items import Scrapy_ModuleItem
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
import os


class Scrapy_ModuleSpider(scrapy.Spider):
    name = "Scrapy_ModuleSpider"
    allowed_domains = ["nwpu.edu.cn"]
    start_urls = ['http://www.nwpu.edu.cn']
    CrawledURL=[]
    SecondCrawledURL=[]
    RecordedURL=[]
    CrawledFileName=None
    CrawledFile=None
    is_FileName=None
    is_File=None
    URLPool=[]
    def __init__(self):
        file_dir = os.path.split(os.path.realpath(__file__))[0]
        self.CrawledFileName = file_dir+'/CrawledURL'
        self.is_FileName = file_dir+'/Filelist'
        self.CrawledFile = open(self.CrawledFileName,'a+')
        Crawled_line = self.CrawledFile.readline().strip().lstrip().rstrip('\n')
        while Crawled_line:
            #print Crawled_line
            self.CrawledURL.append(Crawled_line)
            self.RecordedURL.append(Crawled_line)
            #self.URLPool.append(Crawled_line)
            Crawled_line = self.CrawledFile.readline().strip().lstrip().rstrip('\n')
        self.CrawledFile.close()

    

    def parse(self, response):
        html_doc = response.body 
        html_doc = html_doc.decode('utf-8')
        soup = BeautifulSoup(html_doc)
        #去除网页中的script内容
        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        itemTemp = {}
        itemTemp['title'] = soup.find('title')
        itemTemp['content'] = soup.get_text()
        itemTemp['link'] = soup.findAll("a")
        item = Scrapy_ModuleItem()
        item['cururl'] = response.url
        base_url = get_base_url(response)
        for att in itemTemp:
            item[att] = []
            for obj in itemTemp.get(att):
                if att == 'title':
                    item[att].append(obj.title())
                if att == 'content':
                    item[att] = itemTemp[att]
                if att == 'link':
                    linkhref = obj.get('href')
                    if linkhref:
                        linkhref = urljoin_rfc(base_url, linkhref)
                        if self.url_filter(linkhref):
                            if linkhref in self.URLPool :
                                continue
                            else :
                                #print linkhref
                                item[att].append(linkhref)
                                self.URLPool.append(linkhref)

        if item['cururl'] not in self.RecordedURL:
            yield item
        for url in item['link']:
            #为了发现新链接更新网页库，会爬一次上次已经爬过的地址，但不会储存网页
            if url in self.CrawledURL and url not in self.SecondCrawledURL:
                if not self.is_file(url):
                    self.SecondCrawledURL.append(url)
                    yield Request(url,callback=self.parse)
            elif url not in self.CrawledURL:
                self.CrawledFile = open(self.CrawledFileName,'a+')
                self.CrawledFile.write(url+'\n')
                self.CrawledFile.close()
                self.SecondCrawledURL.append(url)
                self.CrawledURL.append(url)
                if not self.is_file(url):
                    yield Request(url,callback=self.parse)
                else:
                    self.is_File = open(self.is_FileName,'a+')
                    self.is_File.write(url+'\n')
                    self.is_File.close()
#        return item

    #找到从string右边开始第N个substr在string中的索引
    def rfindNStr(self,substr,string,N):
        tergetindex = 0
        while N > 0 :
            index = string.rfind(substr)
            if index == -1:
                return -1
            else :
                string = string[:index-1]  #第一次出现该字符串后后面的字符
                N -= 1
                tergetindex = index       #位置数总加起来
        return tergetindex

    #链接滤除，去掉一下不是文本信息和有效地址的链接
    def url_filter(self,url):
        if 'javascript' in url:
            return False
        if 'mailto' in url:
            return False
        if '.jpg' in url:
            return False
        #http://gs.nwpu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1096673008&wbfileid=370295
        if 'download.jsp' in url:
            return False
        if 'bbs.nwpu.edu.cn' in url:
            if 'forum.php?mod=forumdisplay' in url:
                if len(url) > 60:
                    return False
            elif 'forum.php?mod=viewthread' in url:
                if '&authorid' in url or '&action' in url or '&ordertype' in url:
                    return False
            else:
                return False
        return True

    #判断链接是否为附件
    def is_file(self,url):
        if '.rar' in url:
            return True
        if '.doc' in url:
            return True
        if '.xls' in url:
            return True
        if '.pdf' in url:
            return True
        return False

