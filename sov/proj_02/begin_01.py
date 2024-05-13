import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
from bg_03 import transform
dir_dat = "G:/Programming/Py/sov/proj_02/"
file ="data_02.xlsx" 
df = pd.read_excel(dir_dat+file)
df1 = df.rename(columns={'Treatment':'TR','Treatment_code':'code','Day':'D','Fv/Fm':'TF'})
df1['code']= df1['code'].astype(int)
df1['D']= df1['D'].astype(int)
# print(transform(df1,10))
# df1[['Source', 'Factor', 'Day', 'Val']] = pd.DataFrame(df1['code'].apply(transform).tolist(), index=df1.index)
df1[['Source', 'Factor', 'Day', 'Val']] =\
pd.DataFrame(df1.apply(lambda row: transform(df1, row['code']), axis=1).tolist(), index=df1.index)
# print(df1.head(40))
file= r"G:\Programming\Py\sov\proj_02\data_learn\df1_.xlsx"
df1.to_excel(file)
#  df1[['Source', 'Factor', 'Day', 'Val']] = pd.DataFrame(df1['code'].apply(transform).tolist(), index=df1.index)

"""
Здесь метод apply(transform) вызывает функцию transform для каждой строки df1['code'].
Однако функция transform требует два аргумента, df1 и cod.

df1[['Source', 'Factor', 'Day', 'Val']] = pd.DataFrame(df1['code']
.apply(transform, cod=cod).tolist(), index=df1.index)

df1[['Source', 'Factor', 'Day', 'Val']] = pd.DataFrame(df1.apply(lambda row:
 transform(df1, row['code']), axis=1).tolist(), index=df1.index)

Здесь lambda row: transform(df1, row['code']) создает анонимную функцию, которая принимает строку row из DataFrame и передает значение row['code'] в качестве второго аргумента в функцию transform, вместе с df1.

Это позволяет вам передавать значение cod из каждой строки df1['code'] в функцию transform, чтобы она могла правильно выполниться.

"""
# -----------------------------------------------------------------------------
#   https://chatgpt.com/c/2e22fabe-9e6a-44b5-8abb-47d417a4122c
"""
import pandas as pd
import numpy as np
from scipy import stats

# Создаем исходный DataFrame
data = {
    'Tr': [1, 2, 3, 4, 5, 6],
    'Code': ['A', 'A', 'B', 'B', 'C', 'C'],
    'D': [10, 20, 30, 40, 50, 60],
    'TV': [100, 200, 300, 400, 500, 600]
}
df = pd.DataFrame(data)

# Группируем данные по столбцу Code
grouped = df.groupby('Code')

# Проходим по каждой группе
for name, group in grouped:
    # Проверяем нормальность распределения значений TV в текущей группе
    _, p_value = stats.normaltest(group['TV'])
    if p_value > 0.05:  # Пороговое значение для уровня значимости 0.05
        print(f"Группа {name} имеет нормальное распределение")
    else:
        print(f"Группа {name} НЕ имеет нормальное распределение")

    # Заменяем строки в группе на одну строку со статистикой
    mean_tv = group['TV'].mean()
    max_tv = group['TV'].max()
    std_tv = group['TV'].std()
    group.loc[:, 'TV'] = f"Mean: {mean_tv}, Max: {max_tv}, Std: {std_tv}"

    # Заменяем исходные строки в основном DataFrame
    df.loc[df['Code'] == name, :] = group.iloc[0]

print(df)

"""