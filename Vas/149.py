#
from  random import *
# function to show  sublist 
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print()
# function for creating a nested list of random digits
def rands(m, n):
    res=[[randint(0,9) for i in range(n)] for j in range(m)]
    return res
# function for creating a nested list of letters
def symbs(m, n):
    val='A'
    res=[['' for i in range(n)] for j in range(m)]
    for i in range(m):
        for j in range(n):
            res[i][j]=val
            val=chr(ord(val)+1)
    return res
