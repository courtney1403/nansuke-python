import numpy as np
import pandas as pd
import math
# from make_cnf import MakeCnf
from input_handling import clarifyCells, createXY, getInputChars, makeVariable, getYm, makeSX
from make_cnf import MakeCnf, AtLeastOneValue
from result_decode import ResultDecode

from pysat.solvers import Glucose3
from pysat.formula import CNF
import time
import g_vars
from tohop import TinhToHop

#các biến trong chương trình
#1. Các chuỗi đầu vào: s
#2. Bảng đầu vào: bs (ô trắng/đen)
#3. Mảng X: chuyển đổi i,j thành x. X[x-1] = [i, j]. Máng Y: Y[i,j] = x
#4. Bảng C: lưu các tập hợp dãy ô có độ dài giống nhau lớn hơn 2
#5. Mảng lưu tập hợp các chữ số A
#Cách làm:
#1. Mỗi ô chỉ có 1 số
#2. Điền đúng số trong chuỗi vào các ô: viết cho mỗi tập: C[n] và s[n]
#3. sao cho mỗi số trong chuỗi chỉ được viết 1 lần.

fname = "input13"
with open(fname + ".csv") as file_name:
    g_vars.bs = np.loadtxt(file_name, delimiter=",", dtype = 'int')

df = pd.read_csv(fname + "b.csv") 

for column in df:
	l = df[column].tolist()
	l = [int(x) for x in l if not(math.isnan(x)) == True]
	g_vars.s[int(column)] = l

bs = g_vars.bs
g_vars.Y = np.zeros(bs.shape, dtype = 'int')
start1 = time.time()
n = len(bs)

createXY(bs, n)
clarifyCells(bs, n)
g_vars.A = getInputChars(g_vars.s)
makeSX()

g = Glucose3()
MakeCnf(g, n)

start2 = time.time()
r = g.solve()
print(r)
ym = getYm()
if (r):
	result = g.get_model()
	sb = len(result)
	result = result[:ym]
	r = ResultDecode(result, n)
	np.savetxt('result.csv', r, fmt="%d", delimiter=",")
	end = time.time()
	kq = [end - start1, end - start2, sb, g.nof_clauses(), n, g_vars.countS, g_vars.maxStr, len(g_vars.s)]
	print('Thời gian chạy tổng: ' + str(end - start1))
	print('Thời gian bộ giải: ' + str(end - start2))
	print('Số biến: ' + str(sb))
	print('Số mệnh đề:' + str(g.nof_clauses()))

def getColors(mt, n):
	img = []
	for i in range(len(mt)):
		img.append([])
		for j in range(len(mt[i])):
			if mt[i][j] == -1:
				img[i].append("black")
			else:
				img[i].append("white")
	return img


plt.rcParams["figure.figsize"] = [5.00, 5.00]
plt.rcParams["figure.autolayout"] = True
axs1 = plt.subplot(2,2,1, frameon =False)
axs2 = plt.subplot(2,2,2, frameon =False)
axs3 = plt.subplot(2,2,3, frameon =False)

colors = getColors(bs, n)
axs1.axis('tight')
axs1.axis('off')
the_table1 = axs1.table(cellText=bs, loc='center',cellColours = colors)

colors2 = getColors(r, n)
axs2.axis('tight')
axs2.axis('off')
the_table2 = axs2.table(cellText=r, loc='center',cellColours = colors2)

df = df.replace(np.nan, -1)
for column in df:
	df[column] = df[column].astype(int)
colors3 = getColors(df.values, n)
axs3.axis('tight')
axs3.axis('off')
the_table3 = axs3.table(cellText=df.values, loc='center',cellColours = colors3)

plt.show()