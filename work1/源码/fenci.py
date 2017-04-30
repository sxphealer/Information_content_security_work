#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os
import jieba
import jieba.posseg as pseg
import sys
import string
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
reload(sys)
sys.setdefaultencoding('utf8')
#获取文件列表（该目录下放着33份新闻文档）
def getFilelist(argv) :
    path = argv[1]
    filelist = []
    files = os.listdir(path)
    for f in files :
        if(f[0] == '.') :
            pass
        else :
            filelist.append(f)
    return filelist,path
#对文档进行分词处理
def fenci(argv,path) :
    #保存分词结果的目录
    sFilePath = './segfile'
    if not os.path.exists(sFilePath) : 
        os.mkdir(sFilePath)
    #读取文档
    filename = argv
    f = open(path+filename,'r+')
    file_list = f.read()
    f.close()
    
    #对文档进行分词处理，采用默认模式
    seg_list = jieba.cut(file_list,cut_all=True)

    #对空格，换行符进行处理
    result = []
    for seg in seg_list :
        seg = ''.join(seg.split())
        if (seg != '' and seg != "\n" and seg != "\n\n") :
            result.append(seg)

    #将分词后的结果用空格隔开，保存至本地。
    f = open(sFilePath+"/"+filename+"-seg.txt","w+")
    f.write(' '.join(result))
    f.close()


if __name__ == "__main__" : 
    (allfile,path) = getFilelist(sys.argv)
    for ff in allfile :
        print "Using jieba on "+ff
        fenci(ff,path)