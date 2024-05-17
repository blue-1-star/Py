import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

# Загружаем данные
dir_dat = "G:/Programming/Py/sov/proj_02/"
file = "data_02.xlsx"
df = pd.read_excel(dir_dat + file)

# Переименовываем столбцы
df1 = df.rename(columns={'Treatment': 'TR', 'Treatment_code': 'code', 'Day': 'D', 'Fv/Fm': 'TF'})
df1['code'] = df1['code'].astype(int)
df1['D'] = df1['D'].astype(int)
df2 = df1.copy()

# Применяем функцию analyze_string
df2[['Source', 'Factor', 'Day']] = pd.DataFrame(df2.apply(lambda row: analyze_string(row['TR']), axis=1).tolist(), index=df2.index)

# Сохраняем результаты
file = r"G:\Programming\R\sov\proj_02\df2_.xlsx"
# df2.to_excel(file)


# Группируем данные по столбцу 'code'
grouped = df2.groupby('code')

# Словарь для хранения статистик
statistics = {'Source': [], 'Factor': [], 'Mean': [], 'Max': [], 'Min': [], 'Std': []}

# Рассчитываем статистики для каждой группы
for code, group in grouped:
    mean_tf = group['TF'].mean()
    max_tf = group['TF'].max()
    min_tf = group['TF'].min()
    std_tf = group['TF'].std()
    
    statistics['Source'].append(group['Source'].iloc[0])
    statistics['Factor'].append(group['Factor'].iloc[0])
    statistics['Mean'].append(mean_tf)
    statistics['Max'].append(max_tf)
    statistics['Min'].append(min_tf)
    statistics['Std'].append(std_tf)

# Преобразуем статистики в DataFrame
stats_df = pd.DataFrame(statistics)
# print(stats_df)
sources = stats_df['Source']
factors = stats_df['Factor']
cat = [stats_df['Factor']]
width = 0.3
x = np.arange(len(factors))
fig, ax = plt.subplots()
# Создаем столбцы для каждого Source
for i, source in enumerate(sources):
    means = stats_df[stats_df['Source'] == source]['Mean']
    ax.bar(x + i * width, means, width, label=source)
# r1 = ax.bar(x, stats_df['Mean'],  width, label='1' )
# r2 = ax.bar(x, stats_df['Source'], width, label='2' )
ax.set_xticks(x + width / 2 * (len(sources) - 1))
ax.set_xticklabels(factors)
ax.set_xlabel('Factor')
ax.set_ylabel('Mean')
ax.legend(title='Source')
plt.tight_layout()
plt.show()

"""
имеется датафрейм stats_df
Необходимо построить групповую столбчатую диаграмму
для группы stats_df['Source'] для факторов из stats_df['Factor'] 
по оси y - будут отображаться столбцы высотой stats_df['Mean'] 
"""

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Пример данных stats_df
data = {
    'Source': ['A', 'A', 'B', 'B'],
    'Factor': ['X', 'Y', 'X', 'Y'],
    'Mean': [1.2, 2.3, 1.8, 2.1]
}

stats_df = pd.DataFrame(data)

# Получаем уникальные значения для Source и Factor
sources = stats_df['Source'].unique()
factors = stats_df['Factor'].unique()

# Определяем положение на оси X для каждой группы
x = np.arange(len(factors))
width = 0.3  # Ширина каждого столбца

fig, ax = plt.subplots()

# Создаем столбцы для каждого Source
for i, source in enumerate(sources):
    means = stats_df[stats_df['Source'] == source]['Mean']
    ax.bar(x + i * width, means, width, label=source)

# Настройки осей и меток
ax.set_title('Пример групповой столбчатой диаграммы')
ax.set_xticks(x + width / 2 * (len(sources) - 1))
ax.set_xticklabels(factors)
ax.set_xlabel('Factor')
ax.set_ylabel('Mean')
ax.legend(title='Source')

plt.tight_layout()
plt.show()

"""

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Пример данных stats_df
data = {
    'Source': ['A', 'A', 'B', 'B'],
    'Factor': ['X', 'Y', 'X', 'Y'],
    'Mean': [1.2, 2.3, 1.8, 2.1]
}

stats_df = pd.DataFrame(data)

# Создаем сводную таблицу
pivot_df = stats_df.pivot(index='Factor', columns='Source', values='Mean')

# Получаем уникальные факторы и источники
factors = pivot_df.index
sources = pivot_df.columns

# Определяем положение на оси X для каждой группы
x = np.arange(len(factors))
width = 0.3  # Ширина каждого столбца

fig, ax = plt.subplots()

# Создаем столбцы для каждого Source
for i, source in enumerate(sources):
    means = pivot_df[source]
    ax.bar(x + i * width, means, width, label=source)

# Настройки осей и меток
ax.set_title('Пример групповой столбчатой диаграммы')
ax.set_xticks(x + width / 2 * (len(sources) - 1))
ax.set_xticklabels(factors)
ax.set_xlabel('Factor')
ax.set_ylabel('Mean')
ax.legend(title='Source')

plt.tight_layout()
plt.show()

"""