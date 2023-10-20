nums={100:"сто",1:"один",10:"десять"}
print(nums)
print("1: ", nums[1])
nums[3]="три"
nums[10] = "ten"
print(nums)
nums.pop(100)
print(nums)
# p 195
age=dict([["Кот Матроскин",5],["Пес Шарик",7],["Дядя Федя",12]])
# Перебор ключей
for s in age.keys():
    print(s+":", age[s])
# Перебор значений
for v in age.values():
    print(v, end=" ")    
print()
# Listing 4.12   Генераторы словарей
# Список значений ключей
days=["Пн","Вт","Ср","Чт","Пт","Сб","Вс"] 
week={days[s]: s for s in range(len(days))}
myweek={d: days.index(d) for d in days}
print(week)
print(myweek)
# Creating another dictionary
sqrs={k: k**2 for k in range(1,11) if k%2!=0}
print(sqrs)
# Листинг 4.13. Создание словаря на основе словаря
A = {"Begin":1,"Middle":2,"Last":3}
B=dict(A)
C=A.copy()
D={k: v*10 for k, v in A.items()}
print("A =", A)
print("B =", B)
print("C =", C)
print("D =", D)
for k in A:
    A[k]*=100
print("A =", A)
print("B =", B)
print("C =", C)
print("D =", D)    

