# ex 06 ch 03  p 170
from  random import *
seed(17)
def rands(m, n):
    res=[[randint(0,55) for i in range(n)] for j in range(m)]
    return res
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print() 
def change(A,i,j):
    A.insert(i, A.pop(j))

A = rands(1,9)
show(A)
print("--------")
change(A,2,3)
show(A)
