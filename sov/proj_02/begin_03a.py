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

# Создаем графики для каждой группы 'code'
for code, data in grouped:
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Создаем столбчатую диаграмму для каждой группы
    ax.bar(data['Source'], data['Mean'], label=f"Code: {code}", color='skyblue')
    
    ax.set_xlabel('Source')
    ax.set_ylabel('Mean TF')
    ax.set_title(f'Statistics for Code: {code}')
    ax.legend()
    
    plt.tight_layout()
    plt.show()
