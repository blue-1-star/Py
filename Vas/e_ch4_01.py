#генерируется 15 случайных целых
#чисел: 5 чисел попадают в диапазон значений от 1 до 10 и 10 чисел попадают в диапазон от 10 до 30.
from random import *
def gen_rnd(count, N,M):
    seed(17)
    A = set()
    while len(A) < count: 
        A.add( randint(N,M) )
    return A
    #
A = gen_rnd(5,1,10)
print("A: ",A)
B = gen_rnd(10,10,30)
print("B: ",B)
C = A | B
print(C)



    
