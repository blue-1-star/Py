# Листинг 2.13. Знакомство с обработкой исключений
try:
    num=int(input("Введите целое число: "))
    print("You enter number ",str(num))
except:
    print("You needed to enter an integer")
print("Thanks!")
