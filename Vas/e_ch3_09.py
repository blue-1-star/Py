from  random import *
N=18
seed(17)
A = [randint(0,98) for i in range(N)]
B=[]
def insert_sum(A):
    for i in range(N-1):      
        s = A[i]+A[i+1]
        B.append(s)
    for i in range(N-1):
        k=0
        A.insert(i+k,B[i])
        k+=1
    return A
print(A)
C=insert_sum(A)
print("Result: ",C)
