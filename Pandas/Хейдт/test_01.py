import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
excel_file_path = "G:\\Programming\\Py\Misc\\my.xlsx"
# df = pd.read_excel(excel_file_path)
df = pd.read_excel(excel_file_path, sheet_name="Sheet5")
print(df)
pd.set_option('display.max_columns', 8)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 80)
s = pd.Series([1,2,3,4])
print(s)
print(s[[1,3]])
# p 84 Series
s1 = pd.Series(np.arange(0, 5), index=list('abcde'))
print("s1=\n", s1)
logical_results = s1 >= 3
# print(logical_results)
# print(s1[logical_results])
print(s1[s1>5])
print(s1[(s1 >=2) & (s1 < 5)])
# p 86
# 
np.random.seed(123456)
s2 = pd.Series(np.random.randn(5))
print(s2)
s2.index = ['a', 'b', 'c', 'd', 'e']
print(s2)
# p 88 --------------------------------
s3 = pd.Series([0, 1, 2], index=[0, 1, 2])
s4 = pd.Series([3, 4, 5], index=['0', '1', '2'])
print(s3 + s4)
s4.index = s4.index.values.astype(int)
print(s3 + s4)
