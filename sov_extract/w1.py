def col_name():
    # возвращает список для  столбцов датафрейма 
    return [
        "Filename", 
        "Substrate",
        "Bright_P_mean",
        "Bright_P_std", 
        "Bright_Sq_m", 
        "Bright_Sq_s", 
        "Bright_Cl_m", 
        "Bright_Cl_s", 
        "color_ellips"]
"""
Необходимо визуализировать данные датафрейма 
Группировка по Filename  ( 16 групп ) , Substrate ( 2 группы) 



ось Y   -   показать 2 группы триад - согласно группировке по Substrate
            в каждой 
            Bright_P_mean, Bright_Sq_m, Bright_Cl_m  с усиками соответсвенно Bright_P_std 
            (стандартное отклонение) Bright_Sq_s, Bright_Cl_s   

ось X   -  label (  extract digital part Filename  ) 

Другими словами 
по оси X  располагаем для каждой метки Filename  6 столбиков ( по 3 для каждого Substrate) с пробелом 
между ними чтобы было визуальное отделение различных подгрупп
Итого будет 16 наблюдений ( по 6 = 3 + 3 в каждом гнезде)

Я вижу как коряво формулирую задачу - было бы полезно если бы  ты понял и сформулировал в более 
строгих и научных терминах
"""
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # Пример данных (замените на ваш датафрейм)
# data = pd.DataFrame({
#     "Filename": ["file_1", "file_1", "file_2", "file_2", "file_3", "file_3"],
#     "Substrate": ["A", "B", "A", "B", "A", "B"],
#     "Bright_P_mean": [10, 12, 11, 13, 9, 14],
#     "Bright_P_std": [1, 2, 1.5, 2.5, 1, 3],
#     "Bright_Sq_m": [5, 6, 7, 8, 6, 7],
#     "Bright_Sq_s": [0.5, 1, 0.7, 1.2, 0.6, 1.1],
#     "Bright_Cl_m": [8, 9, 7, 10, 8, 11],
#     "Bright_Cl_s": [1, 1.5, 1.2, 1.8, 1.1, 2]
# })

# # Извлечение числовой части из Filename
# data['Label'] = data['Filename'].str.extract('(\d+)').astype(int)

# # Уникальные метки и субстраты
# labels = data['Label'].unique()
# substrates = data['Substrate'].unique()
# metrics = ['Bright_P_mean', 'Bright_Sq_m', 'Bright_Cl_m']  # Показатели для отображения

# # Настройка графика
# fig, ax = plt.subplots(figsize=(14, 6))
# x = np.arange(len(labels))  # Позиции меток по оси X
# width = 0.12  # Ширина столбцов
# colors = ['skyblue', 'lightgreen', 'lightcoral']  # Цвета для показателей

# # Отображение данных
# for i, substrate in enumerate(substrates):
#     for j, metric in enumerate(metrics):
#         # Фильтрация данных для текущего Substrate и метрики
#         subset = data[data['Substrate'] == substrate]
#         means = subset[metric]
#         stds = subset[metric.replace('_m', '_s')]  # Соответствующее стандартное отклонение
        
#         # Позиция столбцов на графике
#         pos = x + (i * len(metrics) + j) * width
#         ax.bar(pos, means, width, label=f'{substrate} {metric}', color=colors[j], yerr=stds, capsize=5)

# # Настройка осей и легенды
# ax.set_xticks(x + width * (len(substrates) * len(metrics) - 1) / 2)
# ax.set_xticklabels(labels)
# ax.set_xlabel('Filename (Label)')
# ax.set_ylabel('Values')
# ax.legend(title='Substrate and Metric', bbox_to_anchor=(1.05, 1), loc='upper left')

# # Добавление разделителей между группами Filename
# for label in x[1:]:
#     ax.axvline(label - 0.5, color='gray', linestyle='--', linewidth=0.5)

# plt.tight_layout()
# plt.show()   



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Пример данных (замените на ваш датафрейм)
data = pd.DataFrame({
    "Filename": ["file_1", "file_1", "file_2", "file_2", "file_3", "file_3"],
    "Substrate": ["A", "B", "A", "B", "A", "B"],
    "Bright_P_mean": [10, 12, 11, 13, 9, 14],
    "Bright_P_std": [1, 2, 1.5, 2.5, 1, 3],
    "Bright_Sq_m": [5, 6, 7, 8, 6, 7],
    "Bright_Sq_s": [0.5, 1, 0.7, 1.2, 0.6, 1.1],
    "Bright_Cl_m": [8, 9, 7, 10, 8, 11],
    "Bright_Cl_s": [1, 1.5, 1.2, 1.8, 1.1, 2]
})

# Извлечение числовой части из Filename
data['Label'] = data['Filename'].str.extract('(\d+)').astype(int)

# Уникальные метки и субстраты
labels = data['Label'].unique()
substrates = data['Substrate'].unique()

# Сопоставление показателей и их стандартных отклонений
metric_std_map = {
    "Bright_P_mean": "Bright_P_std",
    "Bright_Sq_m": "Bright_Sq_s",
    "Bright_Cl_m": "Bright_Cl_s"
}

# Настройка графика
fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(labels))  # Позиции меток по оси X
width = 0.12  # Ширина столбцов
colors = ['skyblue', 'lightgreen', 'lightcoral']  # Цвета для показателей

# Отображение данных
for i, substrate in enumerate(substrates):
    for j, metric in enumerate(metric_std_map.keys()):
        # Фильтрация данных для текущего Substrate и метрики
        subset = data[data['Substrate'] == substrate]
        means = subset[metric]
        stds = subset[metric_std_map[metric]]  # Соответствующее стандартное отклонение
        
        # Позиция столбцов на графике
        pos = x + (i * len(metric_std_map) + j) * width
        ax.bar(pos, means, width, label=f'{substrate} {metric}', color=colors[j], yerr=stds, capsize=5)

# Настройка осей и легенды
ax.set_xticks(x + width * (len(substrates) * len(metric_std_map) - 1) / 2)
ax.set_xticklabels(labels)
ax.set_xlabel('Filename (Label)')
ax.set_ylabel('Values')
ax.legend(title='Substrate and Metric', bbox_to_anchor=(1.05, 1), loc='upper left')

# Добавление разделителей между группами Filename
for label in x[1:]:
    ax.axvline(label - 0.5, color='gray', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.show()



def visualize_data(data):
    """
    Визуализирует данные датафрейма в виде группированных столбцов с error bars.

    Параметры:
        data (pd.DataFrame): Датафрейм с колонками:
            - Filename: Имя файла (например, "file_1", "file_2").
            - Substrate: Группа (например, "A", "B").
            - Bright_P_mean, Bright_Sq_m, Bright_Cl_m: Средние значения.
            - Bright_P_std, Bright_Sq_s, Bright_Cl_s: Стандартные отклонения.
    """
    # Извлечение числовой части из Filename
    data['Label'] = data['Filename']    #.str.extract('(\d+)').astype(int)

    # Уникальные метки и субстраты
    labels = data['Label'].unique()
    substrates = data['Substrate'].unique()

    # Сопоставление показателей и их стандартных отклонений
    metric_std_map = {
        "Bright_P_mean": "Bright_P_std",
        "Bright_Sq_m": "Bright_Sq_s",
        "Bright_Cl_m": "Bright_Cl_s"
    }

    # Настройка графика
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(labels))  # Позиции меток по оси X
    width = 0.12  # Ширина столбцов
    colors = ['skyblue', 'lightgreen', 'lightcoral']  # Цвета для показателей

    # Отображение данных
    for i, substrate in enumerate(substrates):
        for j, metric in enumerate(metric_std_map.keys()):
            # Фильтрация данных для текущего Substrate и метрики
            subset = data[data['Substrate'] == substrate]
            means = subset[metric]
            stds = subset[metric_std_map[metric]]  # Соответствующее стандартное отклонение
            
            # Позиция столбцов на графике
            pos = x + (i * len(metric_std_map) + j) * width
            ax.bar(pos, means, width, label=f'{substrate} {metric}', color=colors[j], yerr=stds, capsize=5)

    # Настройка осей и легенды
    ax.set_xticks(x + width * (len(substrates) * len(metric_std_map) - 1) / 2)
    ax.set_xticklabels(labels)
    ax.set_xlabel('Filename (Label)')
    ax.set_ylabel('Values')
    ax.legend(title='Substrate and Metric', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Добавление разделителей между группами Filename
    for label in x[1:]:
        ax.axvline(label - 0.5, color='gray', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()