import numpy as np
import g_vars

def decodeCell(x):
	return g_vars.X[x-1]

def decodeVariable(v):
	A = g_vars.A
	n = len(A)
	k = (v - 1)%n
	x = (v-1)/n + 1
	ij = decodeCell(int(x))
	i = ij[0]
	j = ij[1]
	k = A[k]
	return [i, j, int(k)]	

def ResultDecode(result, n):
	ar = np.ones((n, n), dtype = int)
	arr = np.negative(ar)
	# print(arr)
	for x in result:
  		if (x > 0):
	  		r = decodeVariable(x)
	  		# print(r)
	  		arr[r[0], r[1]] = r[2]
	  		# print(arr[r[0]-1, r[1]-1])
	return arr