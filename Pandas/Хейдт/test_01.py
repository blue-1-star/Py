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

