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

# Проверяем максимальное значение кода
max_code = df2['code'].max()
Max_Code = 50  # Установите ваше максимальное значение кода

if max_code <= Max_Code:
    new_data = []
    new_sources = ['U3', 'U4', 'U5']
    new_days = [7, 10, 14]
    new_factors = ['N', 'H', 'F']
    
    for source in new_sources:
        for factor in new_factors:
            for day in new_days:
                # Находим среднее и стандартное отклонение для соответствующих данных
                if source == 'U3':
                    existing_source = 'N0'
                elif source == 'U4':
                    existing_source = 'N1'
                elif source == 'U5':
                    existing_source = 'N2'
                
                existing_data = df2[df2['Source'] == existing_source]['TF']
                mean_tf = existing_data.mean()
                std_tf = existing_data.std()

                for _ in range(10):
                    max_code += 1
                    new_tf_values = np.random.normal(loc=mean_tf, scale=std_tf, size=10)
                    for tf in new_tf_values:
                        new_data.append([max_code, tf, source, factor, day])

    # Создаем датафрейм с новыми данными
    new_df = pd.DataFrame(new_data, columns=['code', 'TF', 'Source', 'Factor', 'Day'])
    df2 = pd.concat([df2, new_df], ignore_index=True)

# Сохраняем обновленный датафрейм
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

# Проверка и замена NaN значений
stats_df.fillna(0, inplace=True)

# Создаем графики
fig, ax = plt.subplots(figsize=(16, 8))

# Бар график для среднего значения
bar_width = 0.15  # Уменьшаем ширину баров
index = np.arange(len(stats_df))

bar1 = ax.bar(index, stats_df['Mean'], bar_width, label='Mean')

# Добавляем ошибочные полосы
ax.errorbar(index, stats_df['Mean'], yerr=stats_df['Std'], fmt='o', color='r', label='Std Dev')

# Добавляем максимальные и минимальные значения
for i in range(len(stats_df)):
    if np.isfinite(stats_df['Max'][i]) and np.isfinite(stats_df['Min'][i]):
        ax.text(index[i], stats_df['Max'][i] + 0.001, f'{stats_df["Max"][i]:.2f}', ha='center', va='bottom', color='green')
        ax.text(index[i] - 0.2, stats_df['Min'][i], f'{stats_df["Min"][i]:.2f}', ha='right', va='top', color='m', fontsize=8)
        
        ax.scatter(index[i], stats_df['Max'][i], color='green', s=50, zorder=5, marker='^', label='Max' if i == 0 else "")
        ax.scatter(index[i], stats_df['Min'][i], color='m', s=50, zorder=5, marker='v', label='Min' if i == 0 else "")

# Настраиваем оси и заголовки
ax.set_xlabel('Treatment_code')
ax.set_ylabel('Fv/Fm')
ax.set_title('Statistics by Code')
ax.set_xticks(index)
ax.set_xticklabels(stats_df['Source'] + '_' + stats_df['Factor'], rotation=90, ha='center')  # Устанавливаем вертикальное расположение подписей
ax.legend()

# Устанавливаем лимиты для оси Y, чтобы график был сжат по вертикали
ax.set_ylim([stats_df['Mean'].min() - 1.4 * stats_df['Std'].max(), stats_df['Max'].max() + 0.9 * stats_df['Std'].max()])

plt.tight_layout()
plt.show()
"""
Изменения:
Уменьшена ширина баров до 0.15.
Изменено расположение подписей на оси X на вертикальное с помощью rotation=90.
Установлено выравнивание подписей по центру с помощью ha='center'.
Эти изменения должны помочь уместить все данные на графике и сделать его более читаемым.
"""