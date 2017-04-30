# !user/bin/env python
# -*- coding:utf-8 -*-


import re
import os
import jieba
import codecs
import random
import requests
import jieba.posseg as pseg
import networkx as nx
import matplotlib.pyplot as plt
from pylab import mpl


names = {}          # 姓名字典
relationships = {}  # 关系字典
lineNames = []      # 每段内人物关系

# 计算姓名出现次数
jieba.load_userdict("D:\work2/dict.txt")        # 加载字典
with open("D:\work2/dict.txt", 'r') as node_file:
    node_list = [node.decode('utf-8').replace('\n', '') for node in node_file.readlines()]
with codecs.open("D:\work2/source.txt", "r", "utf-8") as f:
    for line in f.readlines():
        poss = pseg.cut(line)       # 分词并返回该词词性
        lineNames.append([])        # 为新读入的一段添加人物名称列表
        for w in poss:
            if w.word in node_list:
                lineNames[-1].append(w.word)        # 为当前段的环境增加一个人物
                if names.get(w.word) is None:
                    names[w.word] = 0
                    relationships[w.word] = {}
                names[w.word] += 1                  # 该人物出现次数加 1

# 计算两人之间的关系度
for line in lineNames:                  # 对于每一段
    for name1 in line:                  
        for name2 in line:              # 每段中的任意两个人
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:     # 若两人尚未同时出现则新建项
                relationships[name1][name2]= 1
            else:
                relationships[name1][name2] = relationships[name1][name2]+ 1        # 两人共同出现次数加 1

# 输出文件
with codecs.open("D:\work2/busan_node.txt", "a+", "utf-8") as f:
    f.write("Id Label Weight\r\n")
    for name, times in names.items():
        f.write(name + " " + name + " " + str(times) + "\r\n")

with codecs.open("D:\work2/busan_edge.txt", "a+", "utf-8") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                f.write(name + " " + v + " " + str(w) + "\r\n")

# 画出关系图
relation = relationships
DG = nx.DiGraph()  # 有向图
DG.add_nodes_from(node_list)  # 添加节点
node_num = len(node_list)
for node1 in node_list:
    for node2 in node_list:
        if node1 == node2:
            continue
        else:
            try:
                weight = relation[node1][node2]
                for i in range(weight):
                    DG.add_edge(node1, node2)
            except:
                continue
try:
    pattern = re.compile(r'<td>(.*?)</td>')
    url = 'http://www.114la.com/other/rgb.htm'
    resp = requests.get(url).text
    Colors = re.findall(pattern, resp)
    colors = random.sample(Colors, node_num)
except:
    colors = None
if colors:
    nx.draw(DG, with_labels=True, node_size=900,node_color=colors)
else:
    nx.draw(DG, with_labels=True, node_size = 900)
plt.savefig(r'D:/work2/1.png')
plt.show()