import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
from bg_03 import transform
dir_dat = "G:/Programming/Py/sov/proj_02/"
file ="data_02.xlsx" 
df = pd.read_excel(dir_dat+file)
# print(df.tail())
# print(df.columns)
# pd.test()
# print(df.Treatment.head())
# print(df.loc['Day 7 UGAN 10 F'])
# print(df.iloc[[9,10]])
# print(df[df.Treatment_code == 10 ])

df1 = df.rename(columns={'Treatment':'TR','Treatment_code':'code','Day':'D','Fv/Fm':'TF'})
df1['code']= df1['code'].astype(int)
df1['D']= df1['D'].astype(int)
# print(df1[:4])
# print(grouped.groups)
def print_groups (group_object):
# итерируем по всем группам, печатая название группы
# и первые пять наблюдений в группе
    for name, group in group_object:
        print (name)
        print (group[:5])
# print_groups(grouped)
# b, e = 10, 20
# b, e = 20, 30
# dfh = df1['TF'][b:e]
# print( df1['code'].head(12))
# print(transform(df1,10))
df1[['Source', 'Factor', 'Day', 'Val']] =\
pd.DataFrame(df1.apply(lambda row: transform(df1, row['code']), axis=1).tolist(), index=df1.index)
     
# grouped = df1.groupby('code')
order = {
    'Day': [7, 10, 14],
    'Source': ['U0', 'U1', 'U2', 'C0'],
    'Factor': ['N', 'F', 'H']
}
def order_index(column, value):
    return order[column].index(value)

# grouped = df1.groupby(['Source', 'Factor', 'Day'])
# for name, group in grouped:
grouped = df1.groupby(['Day', 'Source', 'Factor'], 
sort=True, group_keys=False).apply(lambda x: x.sort_values(by=['Day', 'Source', 'Factor'], 
key=lambda x: x.map(lambda x: order_index(x.name, x))))

grouped = df1.groupby(['Day', 'Source', 'Factor'],
 sort=True, group_keys=False).apply(lambda x: x.sort_values(by=['Day', 'Source', 'Factor'],
  key=lambda x: x.apply(lambda col: order_index(col.name, col.iloc[0]))))
# for (source, factor, day), group in grouped:
    # Создаем новое имя группы, объединяя значения из трех столбцов
    # new_name = f"{source}_{factor}_{day}"
    # Получаем значение из столбца Tr для переименования группы
    # new_name = group['Source'].iloc[0]
    # print(new_name)
    # Создаем график
    # plt.figure(figsize=(8, 4))
#
for (day, source, factor), group in grouped:
    print(f"Day: {day}, Source: {source}, Factor: {factor}")
    print(group)
    print()    
    # Строим гистограмму
    # sns.histplot(group['TV'], bins=10, kde=True, color='skyblue', stat='density')
# print(tdf) 
# n_bins = dfh.max() - dfh.min() + 1
# n_bins = 3
# print(dfh)
# print([x for x in range(1,11)])

# plt.bar([x for x in range(1,11)],dfh)
# plt.bar([1-10],dfh)
# dfh.hist(bins=n_bins)
# plt.show()

# Необходимо сгруппировать данные по частям строки такого вида:
#  Day [7,10,14] | U0, U1, U2 ,C0 | [N,F,H]
# Day 7 U0 N, Day 7 U1 N, ...., Day 14 C0 H   - всего различных элементов 3 * 4 * 3 = 36   
#  в трех группах  
#  

"""
# Создаем исходный DataFrame
data = {
    'Tr': [1, 2, 3, 4, 5, 6],
    'Source': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Factor': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    'TV': [100, 200, 300, 400, 500, 600]
}
df = pd.DataFrame(data)

# Определяем порядок "старшинства" для каждого столбца
order = {
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    'Source': ['U0', 'U1', 'U2', 'C0'],
    'Factor': ['X', 'Y']
}

# Создаем функцию, которая будет возвращать индекс порядка "старшинства" для значения
def order_index(column, value):
    return order[column].index(value)

# Группируем данные и сортируем группы
grouped = df.groupby(['Day', 'Source', 'Factor'], 
sort=True, group_keys=False).apply(lambda x: x.sort_values(by=['Day', 'Source', 'Factor'], 
key=lambda x: x.map(lambda x: order_index(x.name, x))))

# Выводим отсортированные группы
for (day, source, factor), group in grouped:
    print(f"Day: {day}, Source: {source}, Factor: {factor}")
    print(group)
    print()


"""
