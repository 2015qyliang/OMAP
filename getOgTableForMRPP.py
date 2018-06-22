# -*- coding: utf-8 -*-
# copyright: qyliang
# time: 06-22-2018

import os
import pandas as pd
from pandas import Series
from pandas import DataFrame

# 路径根据情况替换
filePath = r'E:\OMAP\sortResult'
fileNameList = os.listdir(filePath)

# 定义OgTotal函数
def OgTotal(filePath):
    ogList = []
    for fn in fileNameList:
        os.chdir(filePath)
        dframe = pd.read_csv(fn, sep='\t', header = None)
        firstColumn = dframe.iloc[:,0]
        ogList.extend(list(firstColumn))
    OgList = Series(list(set(ogList)))
    return OgList

# 定义TabDict函数，将tab文件中的信息储存到字典中
def TabDict(filename):
    os.chdir(filePath)
    dframe = pd.read_csv(filename, sep='\t', header=None)
    tabDict = {}
    for i in range(dframe.shape[0]):
        key = dframe.iloc[i, 0]
        value = dframe.iloc[i, 1]
        tabDict[key] = value
    return tabDict

# 定义ExportTable函数
def ExportTable(filename):
    fnFirst = filename.split('.')[0]
    fnFirst = []
    tabDict = TabDict(filename)
    OgList = OgTotal(filePath)
    for i in range(len(OgList)):
        og = OgList[i]
        if og in tabDict:
            fnFirst.append(tabDict[og])
        elif og not in tabDict:
            fnFirst.append(0)
        else:
            pass
    seriesFnFirst = Series(fnFirst)
    return seriesFnFirst

# 程序运行部分
table = DataFrame()
OgList = OgTotal(filePath)
table['OG'] = OgList
for fn in fileNameList:
    tabDict = TabDict(fn)
    seriesFnFirst = ExportTable(fn)
    table[fn] = seriesFnFirst
os.chdir(r'E:\OMAP')
table.to_csv('OgTableForMRPP.txt')

