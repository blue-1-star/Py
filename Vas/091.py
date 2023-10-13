#Листинг 2.8. Решение линейного уравнения
a, b = eval(input("enter (hyphenate) two numbers : "))
if (type(a)==int or type(a)==float) and (type(b)==int or type(b)==float):
    print("equation " + str(a)+"x="+str(b))
    if a!=0:
        print("Решение x="+str(b/a))
    else:
        if b!=0:
            print("No solutions!")
        else:
            print("Solution ia any number")
else:
    print("Incorrect values entered")
    raise SystemExit(0)
print("solution search is complete")


