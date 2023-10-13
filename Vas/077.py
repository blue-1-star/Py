# Простое число
number = int(input("Enter number: "))
num = number//2
k = 2
while k <= num:
    if number%k == 0:
        print("Число не является простым")
        break
    else:
        k += 1
else:
    print("Простое число")
print("Check is complete")    

