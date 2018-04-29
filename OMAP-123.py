# coding: utf-8

import os

# Annotated by blastp with OrthoMCL DB
genomelist = os.listdir('/home/microbiology/inputdata/genome')
count = 0
for gname in genomelist:
		gn = gname.split('.')[0]
		commond_1 = '/home/microbiology/ncbi-blast-2.7.1+/bin/blastp -db /home/microbiology/blast_orthomcl/database/orthomcl -query /home/microbiology/inputdata/genome/'
		commond_2 = gname + ' -evalue 1e-5 -num_threads 24 -max_target_seqs 1 -outfmt 6 -out /home/microbiology/blast_orthomcl/result/' + gn + '.tab'
		commond = commond_1 + commond_2
		count += 1
		print '  ** Total 104 files, On Going:', count, '  **  '
		print gn
		os.system(commond)		
print "  ALL JOBS DONE  "

# Extracted orthologous annotations to form table

namelist = os.listdir('/home/mirco/LIANGDATA/result')
for fn in namelist:
	print('======  ',fn,'  Started  ======')
	os.chdir('/home/mirco/LIANGDATA/result')
	tempog = []
	file = open(fn)
	for line in file.readlines():
		if float(line.split('\t')[2]) >= 40:			   
			tempog.append(line.split('\t')[1] + '\n')
	file.close()
	os.chdir('/home/mirco/LIANGDATA/05-ExtractOrthomcl')
	fnfirst = fn.split('.')[0]
	writefile = fnfirst + '.txt'
	with open(writefile,'w') as file:
		for line in tempog:
			file.write(line)
		file.close()
	print('======  ',fn,'  Done  ======')

os.chdir('/home/mirco')
file = open('headorthomcl.txt')
totalorthomcl = []
for line in file.readlines():
	totalorthomcl.append(line.split('\n')[0])
file.close()

# ExtractOrthomcl
namelist = os.listdir('/home/mirco/LIANGDATA/05-ExtractOrthomcl')
for fn in namelist:
	print('=============',fn)
	os.chdir('/home/mirco/LIANGDATA/05-ExtractOrthomcl')
	file = open(fn)
	orthomcl = []
	for line in file.readlines():
		orthomcl.append(line.split('\n')[0])
	file.close()
	table = []
	print('=============',fn,'   =========  1  ')
	for og in orthomcl:
		for refog in totalorthomcl:
			if (og in refog) and ('group' not in refog):
				table.append(og + '\t' + refog.split('\t')[1])
	newset = set(table)
	newtable = []
	print('=============',fn,'   =========  2  ')
	for nt in newset:
		count = 0
		for tt in table:
			if nt in tt:
				count += 1
		newtable.append(nt + '\t' + str(count) + '\n')
	os.chdir('/home/mirco/LIANGDATA/06-OG')
	with open(fn,'w') as file:
		for line in newtable:
			file.write(line)
		file.close()

# DerepeatOG5
namelist = os.listdir('/home/mirco/LIANGDATA/06-OG')
for fn in namelist:
	os.chdir('/home/mirco/LIANGDATA/06-OG')
	file = open(fn)
	text = []
	for line in file.readlines():
		text.append(line.split('\t')[0])
	file.close()
	setog = set(text)
	newoglist = []
	for og in setog:
		file = open(fn)
		count = 0
		for line in file.readlines():
			if og in line:
				count += int(line.split('\n')[0].split('\t')[1])
		file.close()
		newoglist.append(og + '\t' + str(count) + '\n')
	os.chdir('/home/mirco/LIANGDATA/07-Derepeat')
	with open(fn,'w') as file:
		for line in newoglist:
			file.write(line)
		file.close()

# Build OGsetTable
Table = []
Table.append(totalog)
for fn in namelist:
	os.chdir('/home/mirco/LIANGDATA/06-OG')
	fileofg = []
	file = open(fn)
	for line in file.readlines():
		fileofg.append(line.split('\t')[0])
	file.close()
	countlist = []
	print('============== Searching ... ', fn, '  =============')
	countlist.append(fn.split('.')[0])
	for i in range(1,len(totalog)):
		search = totalog[i]
		if search not in fileofg:
			countlist.append('0')
		elif search in fileofg:
			file = open(fn)
			for line in file.readlines():
				if search in line:
					countlist.append(line.split('\n')[0].split('\t')[1])
			file.close()
		else:
			pass
	Table.append(countlist)
print('============= Writing .............')
print(len(Table))
os.chdir('/home/mirco/LIANGDATA')
with open('02-OGsetTable.txt','w') as file:
	for cl in Table:
		for line in cl:
			file.write(line)
			file.write('\t')
		file.write('\n')
	file.close()

# Form OG5 table
os.chdir('/home/mirco/LIANGDATA')
totalog = []
totalog.append('Species')
file = open('02-OGsetTable.txt')
for line in file.readlines():
	totalog.append(line.split('\n')[0])
file.close()
print(len(totalog))
namelist = os.listdir('/home/mirco/LIANGDATA/07-Derepeat')
Table = []
Table.append(totalog)
for fn in namelist:
	os.chdir('/home/mirco/LIANGDATA/07-Derepeat')
	fileofg = []
	file = open(fn)
	for line in file.readlines():
		fileofg.append(line.split('\t')[0])
	file.close()
	countlist = []
	print('============== Searching ... ', fn, '  =============')
	countlist.append(fn.split('.')[0])
	for i in range(1,len(totalog)):
		search = totalog[i]
		if search not in fileofg:
			countlist.append('0')
		elif search in fileofg:
			file = open(fn)
			for line in file.readlines():
				if search in line:
					countlist.append(line.split('\n')[0].split('\t')[1])
			file.close()
		else:
			pass
	Table.append(countlist)
print('============= Writing .............')
print(len(Table))
os.chdir('/home/mirco/LIANGDATA')
with open('01_ogtable.txt','w') as file:
	for cl in Table:
		for line in cl:
			file.write(line)
			file.write('\t')
		file.write('\n')
	file.close()


print("************************************")
print("*********  All Job Done!  **********")
print("************************************")
