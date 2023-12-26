# p 50 Утиная типизация
def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError: # не допускает итерирования
        return False
print(isiterable([1, 2, 3]))
print(isiterable("a string"))
print(isiterable(5))
template = "{0:.2f} {1:s} are worth US${2:d}"
template.format(88.46, "Argentine Pesos", 1)
