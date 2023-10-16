#   Ex 3  p 170 
from random import *
N = 65
M = 26
def rands(m, n):
    res=[[chr(randint(N,N+M)) for i in range(n)] for j in range(m)]
    return res
def symbs(m, n):
    #val='A'
    val='А'
    res=[['' for i in range(n)] for j in range(m)]
    for i in range(m):
        for j in range(n):
            res[i][j]=val
            val=chr(ord(val)+1)
    return res
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print()    
seed(2001)
A = rands(3,4)
show(A)


