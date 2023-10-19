# ex 08 ch 03  p 170
from  random import *
seed(17)
A = [randint(0,98) for i in range(18)]
print(A)
A1 = A[1::2]
A2=A[::2]
A1s = sorted(A1)
A2s = sorted(A2,reverse=True) 
# print(A1.sort(reverse = True))
# print(A2.sort())
# print(A1s)
# print(A2s)


