import numpy as np
import pandas as pd
# импортируем библиотеку datetime для работы с датами
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
dir_dat = "G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\"
seedval =121232
np.random.seed(seedval)
s = pd.Series(np.random.randn(1096),
index=pd.date_range('2012-01-01',
'2014-12-31'))
walk_ts = s.cumsum()
# walk_ts.plot()
# plt.show()
# сгенерируем данные для столбиковой диаграммы
# сгенерируем небольшую серию, состоящую
# из 10 случайных значений
np.random.seed(seedval)
s = pd.Series(np.random.rand(10) - 0.5)
# строим столбиковую диаграмму
s.plot(kind='bar')
plt.show()
