# Упражнения гл. 2  03
try:
    num=int(input("Введите целое число: "))
    print("number contains ",len(str(num))," digits" )
    #  Exercise 2
    nums = str(num)
    ns = ""
    for k in nums:
        nc = 9 - int(k)
        ns += str(nc)
    print(ns)

except:
    print("You needed to enter an integer")
print("Thanks!")