import numpy as np
import pandas as pd
import math
# from make_cnf import MakeCnf
from binary_cnf import MakeCnf, AtMostOneInRow, AtLeastOneInRow
from result_decode import ResultDecode

from pysat.solvers import Glucose3
from pysat.formula import CNF
import time

def makeVariable(i, j, k, n):
	return (i-1)*n + j-1 + (k-1)*n*n + 1

kqq = []
for x in range(1, 11):
	start1 = time.time()
	#Lấy dữ liệu cho sẵn vào file
	with open("input" + str(x) + ".csv") as file_name:
	# with open("input10.csv") as file_name:
	    ip = np.loadtxt(file_name, delimiter=",", dtype = 'int')

	n = len(ip)
	p = [];
	for i in range(0, n):
		for j in range(0, n):
			if (ip[i][j] != 0):
				s = makeVariable(i + 1, j + 1, ip[i][j], n)
				p.append(int(s))

	# print(p)
	#Khởi tạo bộ giải
	g = Glucose3()
	# n = 36
	#1. Tạo file input.cnf từ đầu vào cho trước
	MakeCnf(g, n)
	#2. Cho file input.cnf vào pysat
	# formula = CNF(from_file='input.cnf')
	# with Glucose3(bootstrap_with=formula.clauses) as g:

	start2 = time.time()
	# print(g.solve())
	print(g.solve(assumptions = p))
	result = g.get_model()

	if (result):
		sb = len(result)
		result = result[:n*n*n]
		# print(result)
		#3. Giải mã kết quả và in ra màn hình
		r = ResultDecode(result, n)
		# print(r)
		# np.savetxt('result.csv', r, fmt="%d", delimiter=",")	
		end = time.time()
		kq = [end - start1, end - start2, sb, g.nof_clauses()]
		kqq.append(kq)

np.savetxt('result2.csv', kqq, delimiter=",")
print(kqq)
	# print(end - start1)
	# print(end - start2)
	# print(sb)
	# print(g.nof_clauses())