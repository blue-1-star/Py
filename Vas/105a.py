#Листинг 2.12. Значения разных типов и тернарный оператор
val=eval(input("Введите выражение: "))
a, b=(val[0], val[-1]) if type(val)==str else (val, type(val))
print(a) 
print(b)

