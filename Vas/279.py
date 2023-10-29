# Листинг 6.12. Использование лямбда-функций
num=10
L=lambda n: 2*n+1
for k in range(num):
    print(L(k), end=" ")
print(L(15))    
L=lambda n: 2**n
print(L(8))
print("grades of two")    
for k in range(num):
    print(L(k), end=" ")
# -----   p 282
def display(f, a, b):
    for k in range(a, b+1):
        print("{0:4}".format(f(k)), end=" ")
    print()
def mypow(n):
    return lambda x: x**n    
def apply(f, h):
    def calc(x):
        return f(h(x))
    return calc    
A=mypow(2)
B=mypow(3)
C=apply(lambda x: 2*x+1, lambda x: 2*x)
print("x ", end="")
display(lambda x: x,1,5)
print("A(x)", end="")
display(A,1,5)
print("B(x)", end="")
display(B,1,5)
print("C(x)", end="")
display(C,1,5)
F=lambda f: lambda x: f(f(x))
print("F(x->x*x)(5): ", F(lambda x: x*x)(5))
print("F(x->2*x+1)(5):", F(lambda x: 2*x+1)(5))
