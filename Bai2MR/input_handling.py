import numpy as np
import pandas as pd
import math
import g_vars
# print(s[2])
#các biến trong chương trình
#1. Các chuỗi đầu vào: s
#2. Bảng đầu vào: bs (ô trắng/đen)
#3. Mảng X: chuyển đổi i,j (i, j chạy từ 0) thành x. X[x-1] = [i, j]. Máng Y: Y[i,j] = x
#4. Bảng C: lưu các tập hợp dãy ô có độ dài giống nhau lớn hơn 2
#5. Mảng lưu tập hợp các chữ số A
#Cách làm:
#1. Mỗi ô chỉ có 1 số
#2. Điền đúng số trong chuỗi vào các ô: viết cho mỗi tập: C[n] và s[n]
#3. sao cho mỗi số trong chuỗi chỉ được viết 1 lần.
def getYm():
	ym = len(g_vars.X) * len(g_vars.A)
	return ym

def createXY(bs, n):
	#Tạo ra mảng X, Y
	# global X, Y
	k = 1
	for i in range(0, n):
		for j in range(0, n):
			if (bs[i,j] != -1):
				g_vars.X.append([i,j])
				g_vars.Y[i][j] = k
				k = k+1
			else:
				g_vars.Y[i][j] = -1
	return 1

def encodeCell(i,j):
	return g_vars.Y[i][j].item()

#xác định tập chữ số đầu vào
def getInputChars(s):
	A = []
	for si in s.values():
		# print(si)
		for it in si:
			st = str(it)
			for char in st:
				A.append(char)

	A = list(dict.fromkeys(A))
	return A

def makeVariable(i, j, k):
	A = g_vars.A
	x = encodeCell(i,j)
	return (x-1)*len(A) + A.index(k) + 1

def makeVariableFromX(x, k):
	A = g_vars.A
	# x = encodeCell(i,j)
	return (x-1)*len(A) + A.index(k) + 1

def makeSX():
  	for key in g_vars.s:
  		for si in g_vars.s[key]:
  			g_vars.sX[si] = g_vars.sX.get(si, 0) + 1
  	return 1

def getStringCount(si):
	return g_vars.sX[si]
	
def saveCi(ci, c):
	# global c
	l = len(ci)
	# return l
	if l >= 2:
		g_vars.countS = g_vars.countS + 1
		if g_vars.maxStr < l:
			g_vars.maxStr = l
		if l in c:
			c[l].append(ci)
		else:
			c[l] = [ci]	
	return 1

def horizontalClarify(bs, n):
	#theo hàng ngang
	for i in range(0, n):
		ci = []
		for j in range(0, n):
			if bs[i][j] == 0: #nếu ô ko phải là ô đen			
				if (j == 0) or (bs[i][j - 1] == -1):
			#nếu là ở mép hoặc ô trước là ô đen thì là đầu chuỗi -> tạo chuỗi mới
					ci = [encodeCell(i,j)]
				else: #nếu không thì tiếp tục chuỗi
					ci.append(encodeCell(i,j))
				# print(ci)
				if (j == n-1): #nếu là cuối dòng thì lưu chuỗi
					saveCi(ci, g_vars.c)
			else: #nếu là ô đen thì lưu chuỗi
				if (ci != []):
					saveCi(ci, g_vars.c)
					ci = []
	return 1

def verticalClarify(bs, n):
	#theo hàng dọc
	for j in range(0, n):
		ci = []
		for i in range(0, n):
			if bs[i][j] == 0: #nếu ô ko phải là ô đen			
				if (i == 0) or (bs[i-1][j] == -1):
			#nếu là ở mép hoặc ô trước là ô đen thì là đầu chuỗi -> tạo chuỗi mới
					ci = [encodeCell(i,j)]
				else: #nếu không thì tiếp tục chuỗi
					ci.append(encodeCell(i,j))
				# print(ci)
				if (i == n-1): #nếu là cuối dòng thì lưu chuỗi
					saveCi(ci, g_vars.c)
			else: #nếu là ô đen thì lưu chuỗi
				if (ci != []):
					saveCi(ci, g_vars.c)
					ci = []
	return 1

def clarifyCells(bs, n):
	horizontalClarify(bs, n)
	verticalClarify(bs, n)
	return 1

def resetVariable():
	g_vars.X = []
	g_vars.c = {}
	g_vars.A = []
	g_vars.s= {}
	g_vars.countS = 0
	g_vars.maxStr = 0

