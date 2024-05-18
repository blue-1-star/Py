import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

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
fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# График 1: Влияние факторов на источники
colors = ['b', 'g', 'r', 'c']  # Задаем цвета для каждого источника
for i, day in enumerate(unique_days):
    day_df = stats_df[stats_df['Day'] == day]
    pivot_df = day_df.pivot(index='Factor', columns='Source', values='Mean')
    x = np.arange(len(factors)) + i * (len(factors) + 1)  # добавляем промежуток между днями
    width = 0.2
    for j, source in enumerate(sources):
        means = pivot_df[source]
        axes[0].bar(x + j * width, means, width, label=f'{source}', color=colors[j], alpha=0.7)
        # Добавляем подписи для каждого дня только на первый график
        if i == 0:
            axes[0].text(x[0] + j * width, means[0], f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для факторов на оси X
axes[0].set_title('Влияние факторов на источники')
axes[0].set_xticks(np.arange(len(factors)) + 0.5)
axes[0].set_xticklabels(factors)
axes[0].set_xlabel('Factor')
axes[0].set_ylabel('Mean')
# Уменьшаем количество элементов в легенде
axes[0].legend(title='Source', ncol=4)

# График 2: Влияние источников на факторы
for i, day in enumerate(unique_days):
    day_df = stats_df[stats_df['Day'] == day]
    pivot_df = day_df.pivot(index='Source', columns='Factor', values='Mean')
    x = np.arange(len(sources)) + i * (len(sources) + 1)  # добавляем промежуток между днями
    width = 0.2
    for j, factor in enumerate(factors):
        means = pivot_df[factor]
        axes[1].bar(x + j * width, means, width, label=f'{factor}', color=colors[j], alpha=0.7)
        # Добавляем подписи для каждого дня только на первый график
        if i == 0:
            axes[1].text(x[0] + j * width, means[0], f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для источников на оси X
axes[1].set_title('Влияние источников на факторы')
axes[1].set_xticks(np.arange(len(sources)) + 0.5)
axes[1].set_xticklabels(sources)
axes[1].set_xlabel('Source')
axes[1].set_ylabel('Mean')
# Уменьшаем количество элементов в легенде
axes[1].legend(title='Factor', ncol=4)

plt.tight_layout()
plt.show()
