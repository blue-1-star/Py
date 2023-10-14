# Листинг 3.11. Поиск и подсчет количества элементов
from random import *
seed(2019)
A=[randint(10,20) for k in range(15)]
print("A:", A)
for a in range(min(A), max(A)+1):
    print(a,"-", A.count(a))
# Max, min, average
print("A[", A.index(min(A)),"]=", min(A), sep="")
print("Max")
print("A[", A.index(max(A)),"]=", max(A), sep="")
print("average:",sum(A)/len(A))
B=sorted(A)
A.sort(reverse=True)
print("A:", A)
print("B:", B)