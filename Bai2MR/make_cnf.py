import numpy as np
import math
from input_handling import makeVariable, makeVariableFromX, getYm
from tohop import TinhToHop
import g_vars

ym = 0
#Tạo thêm biến Tseitin từ cặp ô-chuỗi thứ i
def nextTVariable(ym):
	return ym + 1
#1. Mỗi ô valid chứa chính xác 1 số
def AtLeastOneValue(g, r, c):
	d = []
	n = len(g_vars.A)
	for k in range(0, n):
		#chạy từ Cr1k đến Crnk
		d.append(makeVariable(r,c,g_vars.A[k]))
	g.add_clause(d)	
	return 1

def AtMostOneValue(g, r, c): #r, c cố định, k chạy
	n = len(g_vars.A)
	for k1 in range(0, n - 1):			
		for k2 in range(k1 + 1, n):
			d = []
			d.append(makeVariable(r,c,g_vars.A[k1]) * -1)
			d.append(makeVariable(r,c,g_vars.A[k2]) * -1)
			g.add_clause(d)
			# print(d)
	return 1

#2. Các chuỗi trong s được điền vào các ô theo hướng trái sang phải, trên xuống dưới
#Ta viết biểu thức cho dic s và c
#==> Phần này sẽ gây ra lỗi vì một chữ số có thể bắt đầu nhiều xâu khác nhau 
#==> Cần có biểu thức OR giữa các phép ->
#Luật kéo theo đơn giản
def NumberToCell(g, s, c):
	cs = str(s)
	for l in range(0, 1):
	# for l in range(0, len(cs) - 1):
		x1 = c[l]
		k1 = cs[l]		
		for m in range(l+1, len(cs)):
			d = []
			x = c[m]
			k = cs[m]
			d.append(makeVariableFromX(x1,k1) * -1)
			d.append(makeVariableFromX(x,k))
			g.add_clause(d)
	return 1
#3. Mỗi chuỗi chỉ được điền chính xác 1 lần

def NotAStringCellCouple(s, c):
	d = []
	cs = str(s)
	for m in range(0, len(cs)):
		x = c[m]
		k = cs[m]
		d.append(makeVariableFromX(x,k) * -1)	
	return d

#Hàm này để đặt biến T cho luật kéo theo khi chuỗi s được điền vào chuỗi ô c
#Trong đó:
#Chuỗi s(k1k2k3k4) và ô ci(x1x2x3x4) được điền vào nhau thì sẽ có luật kéo theo:
# x1k1-> (x2k2 & x3k3 & x4k4)
# Đặt: x1k1-> (x2k2 & x3k3 & x4k4) <=> t1
# Mệnh đề tương đương trên sẽ là: 
#1. (-t1 v -x1k1 v x2k2) & (-t1 v -x1k1 v x3k3) & (-t1 v -x1k1 v x4k4)
#2. (x1k1 v t1) & (-x2k2 v -x3k3 v -x4k4 v t1)
def ACoupleKeoTheoT(g, si, ci, t):
# Đặt: x1k1-> (x2k2 & x3k3 & x4k4) <=> t1
	st = str(si)
	x1 = ci[0]
	k1 = st[0]
	x1k1 = makeVariableFromX(x1,k1)
	d2 = []
	for m in range(1, len(st)):
		x = ci[m]
		k = st[m]
		#Mệnh đề: (-t1 v -x1k1 v x2k2) & (-t1 v -x1k1 v x3k3) & (-t1 v -x1k1 v x4k4)
		d1 = []
		d1.append(t * -1)
		d1.append(x1k1 * -1)
		d1.append(makeVariableFromX(x,k))
		g.add_clause(d1)
		#Mệnh đề: (-x2k2 v -x3k3 v -x4k4 v t1)
		d2.append(makeVariableFromX(x,k) * -1)
	d2.append(t)
	g.add_clause(d2)
	#(x1k1 v t1)
	d3 = []
	d3.append(t)
	d3.append(x1k1)
	g.add_clause(d3)	
	return 1
#Hàm kéo theo với 1 set các string có cùng kí tự bắt đầu và 1 chuỗi ô Ci
def StringSetKeoTheo(g, s, ci, ym):
	d = []
	for si in s:
		t = nextTVariable(ym)
		ym = ym + 1
		ACoupleKeoTheoT(g, si, ci, t)
		d.append(t)
	g.add_clause(d)	
	return ym		
#Hàm này để đảm bảo một chuỗi được điền ít nhất 1 lần
#Trong đó:
#Chuỗi s(k1k2k3) và ô ci(x1x2x3) được điền vào nhau khi: x1k1 & x2k2 & x3k3
# Đặt: x1k1 & x2k2 & x3k3 <=> t1
# Mệnh đề tương đương trên sẽ là: 
#(-x1k1 V -x2k2 V -x3k3 v t1) && (-t1 & x1k1) & (-t1 & x2k2) & (-t1 & x3k3)
def BeACoupleWithT(g, s, c, t):
	st = str(s)
	d1 = []	
	for m in range(0, len(st)):
		x = c[m]
		k = st[m]
		#Mệnh đề: (-x1k1 V ... V-xiki v t1)
		d1.append(makeVariableFromX(x,k) * -1)
		#Mệnh đề: (-t1 & x1k1) & (-t1 & x2k2) & (-t1 & x3k3)
		d2 = []
		d2.append(t * -1)
		d2.append(makeVariableFromX(x,k))
		g.add_clause(d2)

	d1.append(t)
	g.add_clause(d1)	
	return 1

def AtLeastOneString(g, si, c, ym):
	n = len(c)
	s = str(si)
	d = []
	for ci in c:
		t = nextTVariable(ym)
		ym = ym + 1
		BeACoupleWithT(g, si, ci, t)
		d.append(t)
	g.add_clause(d)
	return ym
#Hàm này để đảm bảo một chuỗi chỉ được điền nhiều nhất một lần
#Trong đó si là chuỗi cần được điền
#c là tập hợp các chuỗi ô có thể điền được
def AtMostOneString(g, si, c):
	n = len(c)
	for k1 in range(0, n):			
		for k2 in range(k1 + 1, n):
			d = NotAStringCellCouple(si, c[k1]) + NotAStringCellCouple(si, c[k2])
			g.add_clause(d)
	return 1

def ExactlyKString(g,si,c,ym):
	#Các hàm tương đương
	n = len(c)
	s = str(si)
	T = []
	for ci in c:
		t = nextTVariable(ym)
		ym = ym + 1
		T.append(t)
		BeACoupleWithT(g, si, ci, t)
	k = g_vars.sX[si]
	m = len(T)
	#AtLeast: to hop chap n-k+1 của true
	CL = TinhToHop(m-k+1, m)
	for cli in CL:
		d = []
		for clj in cli:
			d.append(T[clj])
		g.add_clause(d)

	#AtMost: to hop chap k+1 cua False
	CM = TinhToHop(k+1, m)
	for cmi in CM:
		d = []
		for cmj in cmi:
			d.append(-T[cmj])
		g.add_clause(d)
	return ym

def findString(s, k):
	#Tìm tập chuỗi trong tập s, bắt đầu bằng kí tự k
	r = []
	for si in s:
		st = str(si)
		if st[0] == k:
			r.append(si)
	return r

def MakeCnf(g, n):
  #AtLeastOneValue in a cell với tất cả các cell và giá trị thuộc A
  for r in range(0, n):
  	for c in range(0, n):
  		if (g_vars.bs[r,c] != -1):
  			AtLeastOneValue(g,r,c)
  			AtMostOneValue(g,r,c)

  ym = getYm()
  # Luật kéo theo với tất cả các cặp s và c
  for key in g_vars.s: #với mỗi độ dài chuỗi
  	#với mỗi kí tự trong bộ kí tự --> tìm các chuỗi si bắt đầu bằng kí tự đó
  	for a in g_vars.A:
  		#tìm ra tập chuỗi bắt đầu bằng kí tự
  		s = findString(g_vars.s[key], a)
  		#nếu nhiều chuỗi bắt đầu bằng kí tự đó
  		if len(s) > 1:
  		#Lần lượt với từng chuỗi ô -> áp dụng luật kéo theo với tập s mới 
  			for ci in g_vars.c[key]:
  				ym = StringSetKeoTheo(g, s, ci, ym)
  		elif len(s) == 1:
			 #nếu chỉ có 1 chuỗi bắt đầu bằng kí tự đó
			#Thực hiện luật kéo theo chuỗi đơn với tất cả chuỗi ô
	  	 	for ci in g_vars.c[key]:
	  	 		NumberToCell(g, s[0], ci)					

  # Luật mỗi chuỗi chỉ được điền chính xác 1 lần
  for key in g_vars.sX:
  	si = key
  	k = g_vars.sX[si]
  	ky = len(str(si))
  	if (k == 1):
  		AtMostOneString(g, si, g_vars.c[ky])
  		ym = AtLeastOneString(g, si, g_vars.c[ky], ym)
  	else:
  		ym = ExactlyKString(g, si, g_vars.c[ky], ym)  	
  	
  return 1

