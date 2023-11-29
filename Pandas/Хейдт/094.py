# DataFrame
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
# plt.show()
df = pd.DataFrame(np.array([[10, 11], [20, 21]]))
print(df)
print(df.columns)
# задаем имена столбцов
df = pd.DataFrame(np.array([[70, 71], [90, 91]]),
columns=['Missoula', 'Philadelphia'])
print(df)
# сколько строк?
print(len(df))
print(df.shape)
# sp500 = pd.read_csv("Data/sp500.csv",
sp500 = pd.read_csv("G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\sp500.csv",
index_col='Symbol',
usecols=[0, 2, 3, 7])
print(sp500.head())
print(len(sp500), "  ",sp500.shape)
print(sp500.index)
# извлекаем столбец Sector
print(sp500['Sector'].head())
# извлекаем столбцы Price и Book Value
print(sp500[['Price', 'Book Value']].head())
# получаем строку с меткой индекса MMM,
# которая возвращается в виде объекта Series
print(sp500.loc['MMM'])
# получаем строки MMM и MSFT
# результатом будет объект DataFrame
print(sp500.loc[['MMM', 'MSFT']])
# получаем позиции меток MMM и A в индексе
i1 = sp500.index.get_loc('MMM')
i2 = sp500.index.get_loc('A')
print((i1, i2))
# и извлекаем строки
print(sp500.iloc[[i1, i2]])
# ищем скалярное значение по метке строки
# и метке (имени) столбца
print(sp500.at['MMM', 'Price'])
# ищем скалярное значение по позиции строки
# и позиции столбца
# извлекаем значение в строке 0, столбце 1
print(sp500.iat[0, 1])
# какие строки имеют значения Price < 100?
print(sp500.Price < 100)
print(sp500[sp500.Price < 100])
# извлекаем лишь те строки, в которых
# значение Price < 10 и > 6
r = sp500[(sp500.Price < 10) &
(sp500.Price > 6)] ['Price']
print(r)
# извлекаем строки, в которых переменная Sector
# принимает значение Health Care, а переменная
# Price больше или равна 100.00
r = sp500[(sp500.Sector == 'Health Care') &
(sp500.Price > 100.00)] [['Price', 'Sector']]
print(r)
# отбираем строки с метками индекса ABT и ZTS
# для столбцов Sector и Price
print(sp500.loc[['ABT', 'ZTS']][['Sector', 'Price']])
print(sp500.columns)
# переименовываем столбец Book Value так, чтобы удалить пробел
# программный код возращает копию датафрейма с переименованным
# столбцом
newSP500 = sp500.rename(columns=
{'Book Value': 'BookValue'})
# печатаем первые 2 строки
print(newSP500[:2])
# создаем копию, чтобы исходные данные остались в неизменном виде
sp500_copy = sp500.copy()
# добавляем столбец
sp500_copy['RoundedPrice'] = sp500.Price.round()
print(sp500_copy[:2])

