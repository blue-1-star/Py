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
#  p 112
# возвращаем новый объект DataFrame со столбцами,
# расположенными в обратном порядке
reversed_column_names = sp500.columns[::-1]
print(sp500[reversed_column_names][:5])
# операция выполняется на месте, поэтому создадим копию
#
# создаем объект DataFrame с единственным
# столбцом Price
rounded_price = pd.DataFrame({'Price': sp500.Price.round()})
print(rounded_price[:5])
copy = sp500.copy()
# заменяем данные в столбце Price новыми значениями
# вместо добавления нового столбца
copy.Price = rounded_price.Price
print(copy[:5])
# 113
# операция выполняется на месте, поэтому создадим копию
copy = sp500.copy()
# заменяем данные в столбце Price округленными значениями
copy.loc[:,'Price'] = rounded_price.Price
print(copy[:5])
# пример использования del для удаления столбца
# делаем копию, потому что операция выполняется на месте
copy = sp500.copy()
print(copy.columns)
del copy['Book Value']
copy[:2]
print(copy[:2])
# 114
# пример использования pop для удаления столбца из датафрейма
# делаем копию, потому что операция выполняется на месте
copy = sp500.copy()
# эта строка удалит столбец Sector и возвратит его как серию
popped = copy.pop('Sector')
# столбец Sector удален на месте
print(copy[:2])
# 115
# копируем первые три строки датафрейма sp500
df1 = sp500.iloc[0:3].copy()
# копируем строки в позициях 10, 11 и 2
df2 = sp500.iloc[[10, 11, 2]]
# присоединяем к датафрейму df1 датафрейм df2
#appended = df1.append(df2)   # !!! 235 As of pandas 2.0, append (previously deprecated) was removed.
# pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
appended = pd.concat([df1,df2])
# a = df1.append(df2)
# в результате к строкам первого датафрейма
# будут присоединены строки второго датафрейма
print(appended)
# print(a)
# 
# p 119
# получаем копию первых 5 строк датафрейма sp500
ss = sp500[:5]
print(ss)
# удаляем строки с метками ABT и ACN
afterdrop = ss.drop(['ABT', 'ACN'])
print(afterdrop[:5])
#
# определяем строки, в которых Price > 300
selection = sp500.Price > 300
# выводим информацию о количестве строк и
# количестве строк, которые будут удалены
print((len(selection), selection.sum()))
# для отбора применим побитовое отрицание
# к выражению selection
price_less_than_300 = sp500[~selection]
print(price_less_than_300)



