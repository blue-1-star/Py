"""
функция, которая аргументами получает ссылку на функцию (например, f()) и целое число (например, n).
Результатом является функция, которая вычисляет результат путем
n-кратного применения функции f()
"""
from random import *
seed(1111)
def g(f,n):
    a=[]
    for i in range(n):
        a.append(f())
    return a
def f():
    return(randint(0,10))
print("rand int -",g(f,11))


