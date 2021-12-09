global X, Y, bs
global s
#1. Các chuỗi đầu vào: s
#2. Bảng đầu vào: bs (ô trắng/đen)
#3. Mảng X: chuyển đổi i,j (i, j chạy từ 0) thành x (chạy từ 1). X[x-1] = [i, j]. Máng Y: Y[i,j] = x
#4. Bảng C: lưu các tập hợp dãy ô có độ dài giống nhau lớn hơn 2
#5. Mảng lưu tập hợp các chữ số A
X = []
c = {}
A = []
s= {}
sX = {} #Dictionary lưu số chuỗi giống nhau

#Lưu số chuỗi
countS = 0
maxStr = 0