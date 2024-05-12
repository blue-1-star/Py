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
print(df1.head(40))
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
