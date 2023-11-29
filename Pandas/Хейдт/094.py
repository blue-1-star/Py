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
