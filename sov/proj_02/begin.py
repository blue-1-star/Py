import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
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

df1 = df.rename(columns={'Fv/Fm':'TF','Treatment_code':'code'})
df1['code']= df1['code'].astype(int)
print(df1[:4])
grouped = df1.groupby('code')
# print(grouped.groups)
def print_groups (group_object):
# итерируем по всем группам, печатая название группы
# и первые пять наблюдений в группе
    for name, group in group_object:
        print (name)
        print (group[:5])
# print_groups(grouped)
b, e = 10, 20
# b, e = 20, 30
dfh = df1['TF'][b:e]
# n_bins = dfh.max() - dfh.min() + 1
n_bins = 3
# print(dfh)
# print([x for x in range(1,11)])

plt.bar([x for x in range(1,11)],dfh)
# plt.bar([1-10],dfh)
# dfh.hist(bins=n_bins)
plt.show()



