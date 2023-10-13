# Листинг 3.4. Создание выборки
A=tuple(k for k in range(1,21) if k%3!=0)
print(A)
B=[2**(k//2) if k%2==0 else 3**(k//2) for k in range(15)]
print(B)
#C=[k for k in range(7)]
C=[0 if k==0 or k==1 else k**2 for k in range(13) if not k in [2,5,7]]
print(C)
Alpha=A[::-1]
print(Alpha)
Bravo=B[::2]
print(Bravo)
Charlie=B[1::2]
print(Charlie)
# test create repo git 1