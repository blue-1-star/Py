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
amount = 10
rate = 88.46
currency = "Pesos"
result = f"{amount} {currency} is worth US${amount / rate}"
print(result)
val = "español"
print(val)
val_utf8 = val.encode("utf-8")
print(val_utf8)
type(val_utf8)
print(val_utf8.decode("utf-8"))

