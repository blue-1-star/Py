# ex 08 ch 03  p 170
from  random import *
seed(17)
A = [randint(0,98) for i in range(18)]
print(A)
A1 = A[1::2]
A2=A[::2]
print(A1)
A1s = sorted(A1)
A2s = sorted(A2,reverse=True)

A1.sort(reverse = True)
print("A1: ",A1)
A2.sort()
print("A2: ",A2)
# print(A1s)
# print(A2s)

# GPT Solution:
B = []
for i in range(min(len(A1), len(A2))):
    B.append(A1[i])
    B.append(A2[i])
# Если A2 длиннее A1, добавьте оставшиеся элементы A2
B.extend(A2[len(A1):])
print("B:",B)

# second GPT Solution
C = [item for pair in zip(A1, A2) for item in pair]
# Если A2 длиннее A1, добавьте оставшиеся элементы A2
C.extend(A2[len(A1):])
print("C:",C)
