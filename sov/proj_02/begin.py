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
print(df.iloc[[9,10]])
# print(df[df.Treatment_code == 10 ])

df1 = df.rename(columns={'Fv/Fm':'TF','Treatment_code':'code'})
df1['code']= df1['code'].astype(int)
print(df1[:4])
grouped = df1.groupby('code')
print(grouped.groups)
def print_groups (group_object):
# итерируем по всем группам, печатая название группы
# и первые пять наблюдений в группе
    for name, group in group_object:
        print (name)
        print (group[:5])
print_groups(grouped)



