#
from  random import *
# function to show  sublist 
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print()
# ---
def rands(m, n):
    res=[[randint(0,9) for i in range(n)] for j in range(m)]
    return res
