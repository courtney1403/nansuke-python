import numpy as np
import pandas as pd
import math

A = [1, 2, 3, 4, 5, 6, 7]
queue = []

def toHop(ind, k, n):
	# print("bat dau:")
	global queue
	i = len(ind)
	if i == 0:
		li = -1
	else:
		li = ind[i-1]
	# print('truong hop:' + str(li))
	if i < k:
		for j in range(li + 1, n - k + i + 1):
			# print(j)
			l = []
			l.extend(ind)
			# print(l)
			l.append(j)
			# print(l)
			queue.append(l)
		# print(d)
		r = 0
		queue.pop(0)
	else:
		r = 1
	return r

def TinhToHop(k, n):
	global queue
	queue = []
	#lặp trong hàng đợi
	queue.append([])
	r = 0
	while r == 0:
		# print(queue)
		d = queue[0]
		r = toHop(d, k, n)
	# print(queue)
	return queue

# TinhToHop(3, 7)
# print(queue)