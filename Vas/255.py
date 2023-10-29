from random import *
def show(L, symb):
    for s in L:
        print(symb, s, sep="", end="")
    print(symb)
A=[1,2,3,4,5]
B={'A','B','C','D'} 
C="Python"
D={"A":1,"B":2,"C":3} 
show(A,"|")
show(B,"|")
show(C,"-")
show(D,"#")
def get_nums(n, state):
    if type(n)!=int:
        return []
    if state:
        L=list(2*(k+1) for k in range(n))
    else:
        L=list(2*k+1 for k in range(n))
    return L
print(get_nums(10, True))    
print(get_nums(8, False))    
print(get_nums(12.5, True))

def get_symbs(n):
    if n>10 or n<1:
        num=10
    else:
        num=n
    S=set()
    Nmin=ord("A")
    Nmax=ord("Z")
    while len(S)<num:
        S.add(chr(randint(Nmin, Nmax)))
    return S
seed(2019)        
print(get_symbs(7))
print(get_symbs(-5))
print(get_symbs(13))
# p 261
def show(first, second, third):
    print(f"[1] first  arg -  {first}")
    print(f"[2] second arg -  {second}")
    print(f"[3] third  arg -  {third}")
show(1,2,3)
show(second="B", third="C", first="A")
show(1, third=3, second=2)
# -----------  p 263
def shift(val):
    print("Function shift")
    print("initial value:",val)
    val=["A","B","C"]
    print("final value:",val)
def change(val):
    print("Function change")
    print("initial value:",val)
    if type(val)==list:
        for k in range(len(val)):
            val[k]+=1
    else:
        val+=1
    print("final value:",val)
num=100
L=[10,20,30]
print(f"Variable num={num}")
change(num)
print(f"Variable num after change={num}")
print(f"L = {L}")
shift(L)
print(f"L after shift = {L}")
change(L)
print(f"L after change = {L}")







