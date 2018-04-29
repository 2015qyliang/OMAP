# 需要导入模块
library(lattice)
library(permute)
library(vegan)
# 导入数据
filedata  = read.table('datafile.txt',
                       sep = '\t',
                       header = TRUE)
# 选择数据子集
filedata.dist = vegdist(subset(filedata, select = -Type))
# mrpp分析，注意分组设定
filedata.mrpp = mrpp(filedata.dist,
                     grouping = filedata$Type,
                     permutations = 999)
filedata.mrpp