#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sklearn.externals import joblib
from numpy import *  
import time 
import numpy
import os
import jieba
import jieba.posseg as pseg
import sys
import string
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt  
reload(sys)
sys.setdefaultencoding('utf8')


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

def Tfidf(filelist) :
    path = './segfile/'
    corpus = []  #存取33份新闻的分词结果
    for ff in filelist :
        print ff
        fname = path + ff
        print fname
        f = open(fname,'r+')
        content = f.read()
        f.close()
        corpus.append(content)    

    vectorizer = CountVectorizer()    
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    
    word = vectorizer.get_feature_names() #所有文本的关键字
    weight = tfidf.toarray()              #对应的tfidf矩阵

    clf = KMeans(n_clusters=4)
    s = clf.fit(weight)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=3)             #输出两维
    newData = pca.fit_transform(weight)   #载入N维
    print newData
    a=0
    lines = []
    resName = "d:/kmeansResult.txt"
    with open(resName,'w') as f:
        for newd in newData:
            x = newd[0]
            y = newd[1]
            line = str(x)+' '+str(y)+'\n'
            lines.append(line)
        for l in lines:
            f.write(l)

    #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    # print(clf.inertia_)


def showgic(dataSet, k, centroids, clusterAssment):   #图形化聚类效果
    numSamples, dim = dataSet.shape  
    if dim != 2:  
        print "输入非二维！"  
        return 1  
  
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']  
    if k > len(mark):  
        print "k值过大！出错！"  
        return 1  
  
    # 画出样例  
    for i in xrange(numSamples):  
        markIndex = int(clusterAssment[i, 0])  
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])  
  
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']  
    # 画中心点 
    for i in range(k):  
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)  
  
    plt.show()  

def euclDistance(vector1, vector2):  
    return sqrt(sum(power(vector2 - vector1, 2)))  
  
# 选取随机点作为质心 
def initCentroids(dataSet, k):  
    numSamples, dim = dataSet.shape  
    centroids = zeros((k, dim))  
    for i in range(k):  
        index = int(random.uniform(0, numSamples))  
        centroids[i, :] = dataSet[index, :]  
    return centroids  

def kmeans(dataSet, k):  
    numSamples = dataSet.shape[0]  
    # i第一列存储属于的簇类 
    # 第二列存储质心到样点差值
    clusterAssment = mat(zeros((numSamples, 2)))  
    clusterChanged = True  
  
    ##初始化所有质心 
    centroids = initCentroids(dataSet, k)  
  
    while clusterChanged:  
        clusterChanged = False  
        #对每个样点 
        for i in xrange(numSamples):  
            minDist  = 100000.0  
            minIndex = 0  
            ## 对于每个质心 
            ## 寻找离质心最近的 
            for j in range(k):  
                distance = euclDistance(centroids[j, :], dataSet[i, :])  
                if distance < minDist:  
                    minDist  = distance  
                    minIndex = j  
              
            #更新簇 
            if clusterAssment[i, 0] != minIndex:  
                clusterChanged = True  
                clusterAssment[i, :] = minIndex, minDist**2  
  
        #更新中心点 
        for j in range(k):  
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]  
            centroids[j, :] = mean(pointsInCluster, axis = 0)  
    return centroids, clusterAssment  



if __name__ == "__main__" : 
    (allfile,path) = getFilelist(sys.argv)
    Tfidf(allfile)
    dataSet = []  
    fileIn = open('d:/kmeansResult.txt')  
    for line in fileIn.readlines():  
        lineArr = line.strip().split(' ')  
        dataSet.append([float(lineArr[0]), float(lineArr[1])])  
    dataSet = mat(dataSet)  
    k = 4  
    centroids, clusterAssment = kmeans(dataSet, k)  
    showgic(dataSet, k, centroids, clusterAssment)  