# ex 07 ch 03  p 170
from  random import *
def max_index(A):
    return [max(A),A.index(max(A))]
seed(17)
A = [randint(0,98) for i in range(10)]
print(A)
# print(max(A))
# print("Index =",A.index(max(A)))
print(max_index(A))
