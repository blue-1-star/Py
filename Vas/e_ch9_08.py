"""
с классом, объекты которого можно вызывать.
У объекта класса должно быть поле-список с числовыми значениями,
а результатом метод возвращает полиномиальную сумму. В частности,
если в списке содержатся числа a0, a1, …, an и в качестве аргумента объекту 
при вызове передается значение x, то в качестве результата должно
возвращаться значение a0 + a1x + a2x2 + … + anxn.
"""
from typing import Any


class e_ch9_08a:
    def __call__(self, x, n):
         return x**n
A=e_ch9_08a()    
# print(A(2,3))
class e_ch9_08b:
    s=0
    def __call__(self, x,a):
        s=0
        for k in range(len(self.a)):
            s+=a[k]*x**k
        return s
    def __init__(self,a):  # set polynomial coefficients  a
        self.a=a
a=[1,1,1]
A=e_ch9_08b(a)
print(A(0,a))
