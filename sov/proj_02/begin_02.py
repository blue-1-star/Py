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
    ax.text(index[i], stats_df['Max'][i]+0.001, f'{stats_df["Max"][i]:.2f}',\
    ha='center', va='bottom', color='green')
    ax.text(index[i] - 0.2, stats_df['Min'][i], f'{stats_df["Min"][i]:.2f}',\
    ha='right', va='top', color='m', fontsize=8)
     # Добавляем текстовые метки для среднего значения
    # ax.text(index[i], stats_df['Mean'][i], f'{stats_df["Mean"][i]:.2f}',\
    # ha='center',va='bottom', color='blue', fontsize=8)

    ax.scatter(index[i], stats_df['Max'][i], color='green', s=50, zorder=5, marker='^', label='Max' if i == 0 else "")  # Треугольник
    ax.scatter(index[i], stats_df['Min'][i], color='m', s=50, zorder=5, marker='v', label='Min' if i == 0 else "")    # down


# Настраиваем оси и заголовки
ax.set_xlabel('Code')
ax.set_ylabel('TF')
ax.set_title('Statistics by Code')
ax.set_xticks(index)
ax.set_xticklabels(stats_df['Source'] + '_' + stats_df['Factor'], rotation=45, ha='right')
ax.legend()
# Устанавливаем лимиты для оси Y, чтобы график был сжат по вертикали
# ax.set_ylim([stats_df['Mean'].min() - 2 * stats_df['Std'].max(), stats_df['Max'].max() + stats_df['Std'].max()])
ax.set_ylim([stats_df['Mean'].min() - 1.4 * stats_df['Std'].max(), stats_df['Max'].max() + 0.9 * stats_df['Std'].max()])
plt.tight_layout()
plt.show()

"""
Оператор ax.scatter()
Функция ax.scatter() используется для создания диаграммы рассеяния (scatter plot). Вот синтаксис и основные параметры, которые используются в вашем случае:

python
Copy code
ax.scatter(x, y, color, s, zorder, marker, label)
x: Координаты по оси X для точки.
y: Координаты по оси Y для точки.
color: Цвет точки.
s: Размер точки.
zorder: Порядок прорисовки (чем выше значение, тем выше на графике будет отображена точка).
marker: Форма маркера (например, '^' для треугольника вверх, 'v' для треугольника вниз).
label: Метка для легенды графика.
Условие if else
Рассмотрим оператор ax.scatter() в вашем коде:

python
Copy code
ax.scatter(index[i], stats_df['Max'][i], color='green', s=50, zorder=5, marker='^', label='Max' if i == 0 else "")
Здесь используется условное выражение if else для параметра label:

python
Copy code
label='Max' if i == 0 else ""
Логика этого выражения следующая:

Если текущий индекс i равен 0 (if i == 0), то метка для этой точки будет 'Max'.
В противном случае (else), метка для этой точки будет пустой строкой "".
Причина использования условия
В легенде графика метка (label) отображается только один раз для каждой уникальной категории точек
 (в данном случае, для максимальных значений). Если мы присваиваем метку 'Max' каждой точке,
 то легенда будет содержать повторяющиеся записи. Условие if i == 0 else "" гарантирует,
  что метка 'Max' будет добавлена только к первой точке (i == 0), а остальные точки
  не будут добавлять новых меток в легенду.
"""