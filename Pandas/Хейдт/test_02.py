# drop
# docs   
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html#pandas.DataFrame.drop
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
df = pd.DataFrame(np.arange(12).reshape(3, 4),
                   columns=['A', 'B', 'C', 'D'])
dfc = df.copy()                   
# print(df) 
# inplace bool, default False If False, return a copy. Otherwise, do operation in place and return None.
df_del = df.drop(['B', 'C'], axis=1, inplace=True)  
# df_del = df.drop(['B', 'C'])
print(df)
print(f'inplace=True: must None',{df_del})   # None
# print(df.drop(['B', 'C'], axis=1))
# print(df)                   
print(dfc.drop(columns=['A','D']))
# MultiIndex
midx = pd.MultiIndex(levels=[['llama', 'cow', 'falcon'],
                             ['speed', 'weight', 'length']],
                     codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],
                            [0, 1, 2, 0, 1, 2, 0, 1, 2]])
df = pd.DataFrame(index=midx, columns=['big', 'small'],
                  data=[[45, 30], [200, 100], [1.5, 1], [30, 20],
                        [250, 150], [1.5, 0.8], [320, 250],
                        [1, 0.8], [0.3, 0.2]])
#codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],  -   first three zeros define 0 element 0 level - it is  llama, llama, llama
#codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],  -   second three zeros define 1 ( first) element 0 level - it is  cow, cow, cow
# [0, 1, 2, 0, 1, 2, 0, 1, 2]  - row for 1 level  - 0,1,2     'speed', 'weight', 'length'
# data - раскладывает значения по ячейкам этой  сетки используя указанные два столбца
print(df)                        
print(df.drop(index=('falcon', 'weight')))  # only for falcon drop only weight
print(df.drop(index='cow', columns='small'))  # all level  - cow - drop, and all column - small
print(df.drop(index='length', level=1))
# print(df.drop(index='length'))


