# test compare dataframe in pandas
# Documentation  pandas.DataFrame.compare    
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.compare.html#pandas.DataFrame.compare
import pandas as pd
from pandas import Series, DataFrame, concat, merge
import numpy as np
df = pd.DataFrame(
    {
        "col1": ["a", "a", "b", "b", "a"],
        "col2": [1.0, 2.0, 3.0, np.nan, 5.0],
        "col3": [1.0, 2.0, 3.0, 4.0, 5.0]
    },
    columns=["col1", "col2", "col3"],
)
print(df)
df2 = df.copy()
df2.loc[0, 'col1'] = 'c'
df2.loc[2, 'col3'] = 4.0
print(df2)
print(df.info())
print(df2.info())
print(df.compare(df2))
print(df.compare(df2, result_names=("left", "right")))



