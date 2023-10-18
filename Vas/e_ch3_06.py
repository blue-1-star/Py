# ex 06 ch 03  p 170
from  random import *
from  copy import *

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
#     
def change_any_pair(A,i,j):
    # swapping arbitrary list items i and j
    A.insert(i, A.pop(j))
    A.insert(j+1, A.pop(i+1))
    


# A = rands(1,9)
A = [randint(0,55) for i in range(9)]
# show(A)
print(A)
B=deepcopy(A)
print("--------")
change(A,2,8)
change_any_pair(B,2,8)
print(A)
print("------")
print("B=",B)
# show(A)
