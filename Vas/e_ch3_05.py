# ex 05 ch 03  p 170
from  random import *
seed(1777)
def rands(m, n):
    res=[[randint(0,55) for i in range(n)] for j in range(m)]
    return res
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print()    

dm, dn = 2, 3   # номера удаляемых строки и столбца
A=rands(4,3) 
show(A)
A.pop(dm-1)
print("-------")
show(A)



