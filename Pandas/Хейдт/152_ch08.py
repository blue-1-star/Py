# ЧИСЛЕННЫЕ И СТАТИСТИЧЕСКИЕ МЕТОДЫ
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
sp500 = pd.read_csv("G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\sp500.csv",
index_col='Symbol',
usecols=[0, 2, 3, 7])
omh = pd.read_csv("G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\omh.csv")
# print(omh.head())
# 154
np.random.seed(123456)
# создаем объект DataFrame
df = pd.DataFrame(np.random.randn(5, 4),
columns=['A', 'B', 'C', 'D'])
print(df)
print(df*2)
# 155
# извлекаем первую строку
s = df.iloc[0]
# вычитаем первую строку из каждой строки объекта DataFrame
diff = df - s
print(diff)
# извлекаем строки в позициях с 1-й по 3-ю и только столбцы B и C
subframe = df[1:4][['B', 'C']]
# мы извлекаем небольшой квадрат из середины df
print(subframe)
# демонстрируем, как происходит выравнивание при
# выполнении операции вычитания
print(df - subframe)
# 157
# извлекаем столбец A
a_col = df['A']
print(df.sub(a_col, axis=0))
s = pd.Series(['a', 'a', 'b', 'c', np.NaN])
# подсчитываем количество значений
print(s.count())
# возвращает список уникальных элементов
print(s.unique())
print(s.nunique())
# 158
# вычисляем встречаемость каждого уникального
# значения для нечисловых данных
print(s.value_counts(dropna=False))
# 172 скользящее окно
#  создаем случайное блуждание
np.random.seed(123456)
s = pd.Series(np.random.randn(1000)).cumsum()
print(s[:5])
# s[0:100].plot();
# s[0:100].plot();
# plt.plot(s[0:100])
# https://stackoverflow.com/questions/66121948/matplotlib-plots-not-showing-in-vs-code
# plt.show()
r = s.rolling(window=3)
print(r)
means = r.mean()
print(means[:7])
# means[0:100].plot();
# plt.show()
# 174 
# создаем датафрейм, состоящий из 50 строк и 4 столбцов
# случайных чисел
np.random.seed(123456)
df = pd.DataFrame(np.random.randn(50, 4))
print(df[:5])
# отбираем три случайные строки
print(df.sample(n=3))
# отбираем 10% строк
print(df.sample(frac=0.1))

