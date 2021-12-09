import numpy as np
import pandas as pd
import math
# from make_cnf import MakeCnf
from input_handling import clarifyCells, createXY, getInputChars, makeVariable, getYm, resetVariable
from make_cnf import MakeCnf, AtLeastOneValue
from result_decode import ResultDecode

from pysat.solvers import Glucose3
from pysat.formula import CNF
import time
import g_vars

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
# X = []
# g_vars.s = {2: [15, 51, 35, 53], 3: [153, 315, 513], 4: [1353, 5315]}
# g_vars.s = {2: [23, 25, 33, 45], 3: [123, 213, 321], 4: [2232, 2522, 3254, 3255, 5233,5333], 5: [15511,15512, 15513, 25533, 35533, 35544, 55532, 55545]}

kqq = []
for x in range(1, 14):
	resetVariable()

	fname = "input" + str(x);
	with open(fname + ".csv") as file_name:
	# with open("input10.csv") as file_name:
	    g_vars.bs = np.loadtxt(file_name, delimiter=",", dtype = 'int')

	df = pd.read_csv(fname + "b.csv") 

	for column in df:
		l = df[column].tolist()
		l = [int(x) for x in l if not(math.isnan(x)) == True]
		g_vars.s[int(column)] = l
	# print(g_vars.s)
	bs = g_vars.bs
	g_vars.Y = np.zeros(bs.shape, dtype = 'int')
	# print(bs)
	start1 = time.time()
	n = len(bs)

	createXY(bs, n)
	# print(g_vars.Y)
	# print(g_vars.X)
	# print(bs)
	clarifyCells(bs, n)
	# print(g_vars.c)

	g_vars.A = getInputChars(g_vars.s)
	# print(g_vars.A)

	g = Glucose3()
	# d = [-1, -2, -3]
	# g.add_clause(d)	
	MakeCnf(g, n)

	start2 = time.time()
	r = g.solve()
	# print(r)
	ym = getYm()
	# print(g.solve(assumptions = p))
	if (r):
		result = g.get_model()
		# print(result)
		sb = len(result)
		result = result[:ym]
		r = ResultDecode(result, n)
		# print(r)
		# np.savetxt('result.csv', r, fmt="%d", delimiter=",")
		end = time.time()
		kq = [end - start1, end - start2, sb, g.nof_clauses(), n, g_vars.countS, g_vars.maxStr, len(g_vars.s), len(g_vars.A)]
		# print(kq)
		kqq.append(kq)

np.savetxt('result2.csv', kqq, delimiter=",")
print(kqq)