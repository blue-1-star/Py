
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from scipy import stats
from lib_sov import gen_data, stats_group

# Ваш существующий код для создания stats_df
dir_dat = "G:/Programming/Py/sov/proj_02/"
file = "data_02.xlsx"
df = gen_data(dir_dat + file)
print(df.columns)
# Получаем статистики в сгруппированных по столбцу 'code' данных
stats_df = stats_group(df, 'code')

# Уникальные значения для Day
unique_days = stats_df['Day'].unique()

# Уникальные факторы и источники
factors = stats_df['Factor'].unique()
sources = stats_df['Source'].unique()

# Создаем графики
fig, axes = plt.subplots(2, 1, figsize=(20, 14))

# Ширина столбцов
width = 0.15

# График 1: Влияние факторов на источники
colors = ['b', 'g', 'r', 'c']  # Задаем цвета для каждого источника
for i, day in enumerate(unique_days):
    day_df = stats_df[stats_df['Day'] == day]
    pivot_df = day_df.pivot(index='Factor', columns='Source', values='Mean')
    x = np.arange(len(factors)) * (len(sources) + 1) + i * (len(factors) + 1) * len(sources) * width  # добавляем промежуток между днями
    for j, source in enumerate(sources):
        means = pivot_df[source]
        bars = axes[0].bar(x + j * width, means, width, label=source if i == 0 else "", color=colors[j], alpha=0.7)
    # Добавляем метки для каждого дня
    axes[0].text(np.mean(x) + (len(sources) - 1) * width / 2, max(means) + 0.05, f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для факторов на оси X
xticks = []
for i in range(len(unique_days)):
    for j in range(len(factors)):
        xticks.append(i * (len(factors) + 1) * len(sources) * width + j * (len(sources) + 1) * width / 2)
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
    x = np.arange(len(sources)) * (len(factors) + 1) + i * (len(sources) + 1) * len(factors) * width  # добавляем промежуток между днями
    for j, factor in enumerate(factors):
        means = pivot_df[factor]
        bars = axes[1].bar(x + j * width, means, width, label=factor if i == 0 else "", color=colors[j], alpha=0.7)
    # Добавляем метки для каждого дня
    axes[1].text(np.mean(x) + (len(factors) - 1) * width / 2, max(means) + 0.05, f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для источников на оси X
xticks = []
for i in range(len(unique_days)):
    for j in range(len(sources)):
        xticks.append(i * (len(sources) + 1) * len(factors) * width + j * (len(factors) + 1) * width / 2)
axes[1].set_xticks(xticks)
axes[1].set_xticklabels(np.tile(sources, len(unique_days)))
axes[1].set_title('Влияние источников на факторы')
axes[1].set_xlabel('Source')
axes[1].set_ylabel('Mean')
axes[1].legend(title='Factor', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
