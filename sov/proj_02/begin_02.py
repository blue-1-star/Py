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

# Группируем данные по 'code'
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

# Создаем графики
fig, ax = plt.subplots(figsize=(16,8 ))

# Бар график для среднего значения
bar_width = 0.25
index = np.arange(len(stats_df))

bar1 = ax.bar(index, stats_df['Mean'], bar_width, label='Mean')

# Добавляем ошибочные полосы
ax.errorbar(index, stats_df['Mean'], yerr=stats_df['Std'], fmt='o', color='r', label='Std Dev')

# Добавляем максимальные и минимальные значения
for i in range(len(stats_df)):
    ax.text(index[i], stats_df['Max'][i], f'{stats_df["Max"][i]:.2f}', ha='center', va='bottom', color='green')
    ax.text(index[i], stats_df['Min'][i], f'{stats_df["Min"][i]:.2f}', ha='right', va='top', color='m')

# Настраиваем оси и заголовки
ax.set_xlabel('Code')
ax.set_ylabel('TF')
ax.set_title('Statistics by Code')
ax.set_xticks(index)
ax.set_xticklabels(stats_df['Source'] + '_' + stats_df['Factor'], rotation=45, ha='right')
ax.legend()
# Устанавливаем лимиты для оси Y, чтобы график был сжат по вертикали
ax.set_ylim([stats_df['Mean'].min() - 2 * stats_df['Std'].max(), stats_df['Max'].max() + stats_df['Std'].max()])

plt.tight_layout()
plt.show()

