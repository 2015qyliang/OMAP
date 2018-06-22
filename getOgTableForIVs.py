# -*- coding: utf-8 -*-
# copyright: qyliang
# time: 06-22-2018

import os
import pandas as pd
from pandas import Series
from pandas import DataFrame

# 定义OgIVs函数
def OgIVs(ogfilename):
    ogList = []
    os.chdir(r'E:\OMAP')
    dframe = pd.read_csv(ogfilename, sep='\t', header = None)
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
    OgList = OgIVs(ogfilename)
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

# 路径根据情况替换
filePath = r'E:\OMAP\sortResult'
fileNameList = os.listdir(filePath)
# 程序运行部分
ogfilename = input('请输入ogTable for IVs的文件名(如： og123.txt): ')
table = DataFrame()
OgList = OgIVs(ogfilename)
table['OG'] = OgList
for fn in fileNameList:
    tabDict = TabDict(fn)
    seriesFnFirst = ExportTable(fn)
    table[fn] = seriesFnFirst
os.chdir(r'E:\OMAP')
table.to_csv('OgTableForIVs.txt')

