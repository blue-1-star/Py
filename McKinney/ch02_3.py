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
# p 59 
from datetime import datetime, date, time
dt = datetime(2011, 10, 29, 20, 30, 21)
print(dt.strftime("%d.%m.%Y %H:%M"))
print(dt.strftime("%Y-%m-%d %H:%M"))
datetime.strptime("20091031", "%Y%m%d")
dt_hour = dt.replace(minute=0, second=0)
print(dt_hour)
dt2 = datetime(2011, 11, 15, 22, 30)
delta = dt2 - dt
print(delta)
# p 62 
sequence = [1, 2, None, 4, None, 5]
total = 0
for value in sequence:
    if value is None:
        continue
    total += value
