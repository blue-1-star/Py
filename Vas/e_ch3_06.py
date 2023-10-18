# ex 06 ch 03  p 170
from  random import *
from  copy import *
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
seed(17)
A = [randint(0,55) for i in range(16)]
print(A)
print("--------")
sort_bubble(A)
print(A)
