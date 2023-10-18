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
def change(A,i):
    A.insert(i, A.pop(i+1))
#     
def swap_any_pair(A,i,j):
    # swapping arbitrary list items i and j
    A.insert(i, A.pop(j))
    A.insert(j, A.pop(i+1))
def sort_bubble(A):
    n = len(A)
    k = 0
    while k<n:
        for i in range(n-1-k):
            if A[i]>A[i+1]: change(A,i) 
        k+=1





# A = rands(1,9)
A = [randint(0,55) for i in range(9)]
# show(A)
print(A)
B=deepcopy(A)
print("--------")
change(A,2,3)
# swap_any_pair(B,2,3)
print(A)
# print("------")
# print("B=",B)
# show(A)
