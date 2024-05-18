import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ваш существующий код для создания stats_df
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

# Группируем данные по столбцу 'code'
grouped = df2.groupby('code')

# Словарь для хранения статистик
statistics = {'Source': [], 'Factor': [], 'Day': [], 'Mean': [], 'Max': [], 'Min': [], 'Std': []}

# Рассчитываем статистики для каждой группы
for code, group in grouped:
    mean_tf = group['TF'].mean()
    max_tf = group['TF'].max()
    min_tf = group['TF'].min()
    std_tf = group['TF'].std()
    
    statistics['Source'].append(group['Source'].iloc[0])
    statistics['Factor'].append(group['Factor'].iloc[0])
    statistics['Day'].append(group['Day'].iloc[0])
    statistics['Mean'].append(mean_tf)
    statistics['Max'].append(max_tf)
    statistics['Min'].append(min_tf)
    statistics['Std'].append(std_tf)

# Преобразуем статистики в DataFrame
stats_df = pd.DataFrame(statistics)

# Уникальные значения для Day
unique_days = stats_df['Day'].unique()

# Уникальные факторы и источники
factors = stats_df['Factor'].unique()
sources = stats_df['Source'].unique()

# Создаем графики
fig, axes = plt.subplots(2, 1, figsize=(16, 12))

# Ширина столбцов
width = 0.4

# График 1: Влияние факторов на источники
colors = ['b', 'g', 'r', 'c']  # Задаем цвета для каждого источника
for i, day in enumerate(unique_days):
    day_df = stats_df[stats_df['Day'] == day]
    pivot_df = day_df.pivot(index='Factor', columns='Source', values='Mean')
    x = np.arange(len(factors)) + i * (len(factors) + 1) * len(sources)  # добавляем промежуток между днями
    for j, source in enumerate(sources):
        means = pivot_df[source]
        bars = axes[0].bar(x + j * width, means, width, label=source if i == 0 else "", color=colors[j], alpha=0.7)
    # Добавляем метки для каждого дня
    axes[0].text(np.mean(x) + (len(sources) - 1) * width / 2, max(means) + 0.1, f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для факторов на оси X
xticks = []
for i in range(len(unique_days)):
    for j in range(len(factors)):
        xticks.append(i * (len(factors) + 1) * len(sources) + j * len(sources) + (len(sources) - 1) * width / 2)
axes[0].set_xticks(xticks)
axes[0].set_xticklabels(np.tile(factors, len(unique_days)))
axes[0].set_title('Влияние факторов на источники')
axes[0].set_xlabel('Factor')
axes[0].set_ylabel('Mean')
axes[0].legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')

# График 2: Влияние источников на факторы
for i, day in enumerate(unique_days):
    day_df = stats_df[stats_df['Day'] == day]
    pivot_df = day_df.pivot(index='Source', columns='Factor', values='Mean')
    x = np.arange(len(sources)) + i * (len(sources) + 1) * len(factors)  # добавляем промежуток между днями
    for j, factor in enumerate(factors):
        means = pivot_df[factor]
        bars = axes[1].bar(x + j * width, means, width, label=factor if i == 0 else "", color=colors[j], alpha=0.7)
    # Добавляем метки для каждого дня
    axes[1].text(np.mean(x) + (len(factors) - 1) * width / 2, max(means) + 0.1, f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для источников на оси X
xticks = []
for i in range(len(unique_days)):
    for j in range(len(sources)):
        xticks.append(i * (len(sources) + 1) * len(factors) + j * len(factors) + (len(factors) - 1) * width / 2)
axes[1].set_xticks(xticks)
axes[1].set_xticklabels(np.tile(sources, len(unique_days)))
axes[1].set_title('Влияние источников на факторы')
axes[1].set_xlabel('Source')
axes[1].set_ylabel('Mean')
axes[1].legend(title='Factor', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
