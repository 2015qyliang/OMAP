# -*- coding: utf-8 -*-
# copyright: qyliang
# time: 06-21-2018

import os
import pandas as pd

# 定义blastp函数，无需return
def Blastp():
	os.chdir('/home/microbiology/blast_orthomcl/')
	fileNameList = os.listdir('/home/microbiology/inputdata/')
	blastpPath = '/home/microbiology/ncbi-blast-2.7.1+/bin/blastp'
	proc1 = blastpPath + ' -db /home/microbiology/blast_orthomcl/database/orthomcl -query /home/microbiology/inputdata/'
	proc2 = ' -evalue 1e-5 -num_threads 24 -max_target_seqs 1 -outfmt 6 -out /home/microbiology/blast_orthomcl/result/'
	for fn in fileNameList:
		fnFirst = fn.split('.')[0]
		process = proc1 + fn + proc2 + fnFirst + '.tab'
		print('='*50)
		print('='*10,'Total files: ', len(fileNameList))
		print('='*10,'Current order: ', fileNameList.index(fn) + 1)
		os.system(process)

# 定义函数sortResult,筛选result文件中的信息,需要return
def sortResult():
	os.chdir('/home/microbiology/blast_orthomcl/')
	dframe = pd.read_table('OrthoMCL.txt', sep = '\t')
	ogDict = {}
	for i in range(dframe.shape[0]):
		key = dframe.iloc[i,0].split('>')[1]
		value = dframe.iloc[i,1]
		ogDict[key] = value

	fnNameList = os.listdir('/home/microbiology/blast_orthomcl/result/')

	for fn in fnNameList:
		os.chdir('/home/microbiology/blast_orthomcl/result/')
		dframe1 = pd.read_csv(fn, sep = '\t')
		dframe2 = dframe1[dframe1.iloc[:,2] > 40]
		ogKeys = dframe2.iloc[:,1]
		newOgKeys = []
		for ogk in ogKeys:
			newOgKeys.append(ogDict[ogk])
		ogSet = set(newOgKeys)
		newOgTable = {}
		for og in ogSet:
			newOgTable[og] = newOgKeys.count(og)
		os.chdir('/home/microbiology/blast_orthomcl/sortResult/')
		with open(fn, 'w') as file:
			for k,v in newOgTable.items():
				if k != 'no_group':
					file.write(k + '\t')
					file.write(str(v) + '\n')
			file.close()
		

# 运行程序
Blastp()
sortResult()
