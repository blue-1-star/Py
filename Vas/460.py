# Листинг 9.17. Индексирование объектов
class Alpha:
    def __getitem__(self, index):
        return self.value[index]
    def __setitem__(self, index, val):
        self.value[index]=val
    def __delitem__(self, index):
        del self.value[index]
    def __str__(self):
        return str(self.value)
    def __len__(self):
        return len(self.value)
A=Alpha()
A.value=[100,200,300]
A.r = "fff"
print(A)
for k in range(len(A)):
    print(A[k], end=" ")
print()
A[1]="A"
print(A)
del A[0]
print(A)
# ---------------
# Листинг 9.18. Индексирование объекта для вычисления чисел Фибоначчи
class Fibs:
    def __getitem__(self, n):
        a=1
        b=1
        for k in range(n-2):
            a, b=b, a+b
        return b
F = Fibs()
for k in range(1,16):
    print(F[k], end=" ")
print()
# ---------------
# Листинг 9.19. Вызов объекта
class Alpha1:
    def __call__(self, n):
        s=0
        for k in range(len(self.nums)):
            s+=self.nums[k]**n
        return s
class Alpha2:
    def __call__(self, list1, list2):
        result = sum(x * y for x, y in zip(list1, list2))
        return result
class Alpha3:
    def __call__(self, list1, list2, list3):
        result = sum(x * y * z for x, y, z in zip(list1, list2, list3))
        return result        
class Bravo:
    def __call__(self, x, y):
        return self.num*x+self.val*y  
A=Alpha1()
A.nums=[1,2,3]
print("A(1) =", A(1))
print("A(2) =", A(2))
B=Bravo()
B.num=2
B.val=3              
print("B(5,1) =", B(5,1))
print("B(3,4) =", B(3,4))
#----------------
list_a = [1, 2, 3]
list_b = [4, 5, 6]
list_c = [2, 2, 2]

A2=Alpha2()
print(A2(list_a,list_b))
A3=Alpha3()
print(A3(list_a,list_b, list_c))
