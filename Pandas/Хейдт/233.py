# ГЛАВА 11 ОБЪЕДИНЕНИЕ, СВЯЗЫВАНИЕ И ИЗМЕНЕНИЕ ФОРМЫ ДАННЫХ
import numpy as np
import pandas as pd
# импортируем библиотеку datetime для работы с датами
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
# создаем два объекта Series для конкатенации
s1 = pd.Series(np.arange(0, 3))
s2 = pd.Series(np.arange(5, 8))
print(pd.concat([s1, s2]))
# создаем два объекта DataFrame для конкатенации,
# используя те же самые индексные метки и имена столбцов,
# но другие значения
df1 = pd.DataFrame(np.arange(9).reshape(3, 3),
columns=['a', 'b', 'c'])
#df2 имеет значения 9 .. 18
df2 = pd.DataFrame(np.arange(9, 18).reshape(3, 3),
columns=['a', 'b', 'c'])
print(pd.concat([df1, df2]))
# демонстрируем конкатенацию двух объектов DataFrame
# с разными столбцами
df1 = pd.DataFrame(np.arange(9).reshape(3, 3),
columns=['a', 'b', 'c'])
df2 = pd.DataFrame(np.arange(9, 18).reshape(3, 3),
columns=['a', 'c', 'd'])
# значения столбца b в датафрейме df2
print(pd.concat([df1, df2], sort=True))
# выполняем конкатенацию двух объектов,
# но при этом создаем индекс с помощью
# заданных ключей
c = pd.concat([df1, df2], keys=['df1', 'df2'], sort=True)
# обратите внимание на метки строк в выводе
print(c)
# мы можем извлечь данные, относящиеся к первому
# или второму исходному датафрейму
print(c.loc['df2'])
# конкатенируем датафреймы df1 и df2 по оси столбцов
# выравниваем по меткам строк,
# получаем дублирующиеся столбцы
print(pd.concat([df1, df2], axis=1))
# создаем новый датафрейм df3, чтобы конкатенировать его
# с датафреймом df1
# датафрейм df3 имеет общую с датафреймом df1
# метку 2 и общий столбец a
df3 = pd.DataFrame(np.arange(20, 26).reshape(3, 2),
columns=['a', 'd'],
index=[2, 3, 4])
print(df1)
print(df3)
# конкатерируем их по оси столбцов. Происходит выравнивание по меткам строк,
# осуществляется заполнение значений столбцов df1, а затем
# столбцов df3, получаем дублирующиеся столбцы
print(pd.concat([df1, df3], axis=1))
# выполняем внутреннее соединение вместо внешнего
# результат представлен в виде одной строки
print(pd.concat([df1, df3], axis=1, join='inner'))
# -------------------------------------------------    239
# это наши клиенты
customers = {'CustomerID': [10, 11],
'Name': ['Mike', 'Marcia'],
'Address': ['Address for Mike',
'Address for Marcia']}
customers = pd.DataFrame(customers)
print(customers)
# это наши заказы, сделанные клиентами,
# они связаны с клиентами с помощью столбца CustomerID
orders = {'CustomerID': [10, 11, 10],
'OrderDate': [date(2014, 12, 1),
date(2014, 12, 1),
date(2014, 12, 1)]}
orders = pd.DataFrame(orders)
print(orders)
# выполняем слияние датафреймов customers и orders так, чтобы
# мы могли отправить товары
print(customers.merge(orders))
# ---
# создаем данные, которые будем использовать в качестве примеров
# в оставшейся части этого раздела
left_data = {'key1': ['a', 'b', 'c'],
'key2': ['x', 'y', 'z'],
'lval1': [ 0, 1, 2]}
right_data = {'key1': ['a', 'b', 'c'],
'key2': ['x', 'a', 'z'],
'rval1': [ 6, 7, 8 ]}
left = pd.DataFrame(left_data, index=[0, 1, 2])
right = pd.DataFrame(right_data, index=[1, 2, 3])
print(left)
print(right)
# демонстрируем слияние, не указывая столбцы, по которым
# нужно выполнить слияние
# этот программный код неявно выполняет слияние
# по всем общим столбцам
print(left.merge(right))
# демонстрируем слияние, явно задав столбец,
# по значениям которого нужно связать
# объекты DataFrame
left.merge(right, on='key1')


