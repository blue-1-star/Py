import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from openpyxl import load_workbook
import tempfile
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import friedmanchisquare
from sklearn.cluster import KMeans
from scikit_posthocs import posthoc_dunn


file = r"G:\My\sov\extract\FLinext.xlsx"
output_dir = os.path.join(os.path.dirname(__file__), 'Data')

sheet_name = 0          #"Sheet1"
xls = pd.ExcelFile(file)


# Проверка на существование листа
if isinstance(sheet_name, int):
    if sheet_name >= len(xls.sheet_names):
        raise ValueError("Лист с указанным индексом не существует.")
    sheet_name = xls.sheet_names[sheet_name]
else:
    if sheet_name not in xls.sheet_names:
        raise ValueError(f"Лист с именем '{sheet_name}' не найден. Доступные листы: {xls.sheet_names}")

df = xls.parse(sheet_name="Sheet1")
df = df.drop(df.columns[4], axis=1) # delete column 4
df = df.drop(index =0 ) # delete row  0

# Задаем новые имена столбцам с индексами 1, 2, 3
new_names = {0: 'Meth', 1: 'RP1', 2: 'RP2', 3: 'RP3'}
df.rename(columns={df.columns[i]: new_name for i, new_name in new_names.items()}, inplace=True)
# print(df.columns)
# 1. Создание среднего значения по столбцам RP1, RP2, RP3
df['Average'] = df[['RP1', 'RP2', 'RP3']].mean(axis=1)

# Группировка по столбцу Meth
grouped = df.groupby('Meth')['Average'].apply(list)

# 2. Тест Фридмана
group_values = grouped.values
stat, p_value = friedmanchisquare(*group_values)
print("Тест Фридмана:")
print(f"Статистика: {stat}, p-значение: {p_value}")

posthoc = posthoc_dunn(grouped.values, p_adjust='bonferroni')  # Пост-хок тест Неменя
print(posthoc)
plt.figure(figsize=(16, 12)) 
sns.heatmap(posthoc, annot=True, fmt=".3f", cmap="coolwarm")
plt.title("Post-hoc Test Results",  fontsize=16)
plt.show()


# print( df)
# print( grouped)
