# 8.2. Комбинирование и слияние набо ров данных
# Слияние объектов DataFrame как в базах данных
import numpy as np 
import pandas as pd
df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "a", "b"],
"data1": pd.Series(range(7), dtype="Int64")})
df2 = pd.DataFrame({"key": ["a", "b", "d"],
"data2": pd.Series(range(3), dtype="Int64")})
print(df1)
print(df2)
print(pd.merge(df1, df2))

