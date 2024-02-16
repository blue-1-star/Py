# 8.2. Комбинирование и слияние набо ров данных
# Слияние объектов DataFrame как в базах данных
import numpy as np 
import pandas as pd
# p 260
df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "a", "b"],
"data1": pd.Series(range(7), dtype="Int64")})
df2 = pd.DataFrame({"key": ["a", "b", "d"],
"data2": pd.Series(range(3), dtype="Int64")})
print(df1)
print(df2)
print(pd.merge(df1, df2))
# p 261
# Обратите внимание, что я не указал, по какому столбцу производить соеди-
# нение. В таком случае merge использует в качестве ключей столбцы с одинако-
# выми именами.
df3 = pd.DataFrame({"lkey": ["b", "b", "a", "c", "a", "a", "b"],
"data1": pd.Series(range(7), dtype="Int64")})
df4 = pd.DataFrame({"rkey": ["a", "b", "d"],
"data2": pd.Series(range(3), dtype="Int64")})
print(pd.merge(df3, df4, left_on="lkey", right_on="rkey"))
"""
По умолчанию функция merge производит внутреннее соединение ('inner');
в результирующий объект попадают только ключи, присутствующие в обоих
объектах-аргументах. 
Альтернативы: 'left', 'right' и 'outer'. В случае внешнего соединения ('outer')
берется объединение ключей, т. е. получается то же самое, что при совместном
применении левого и правого соединений:
"""
print(pd.merge(df1, df2, how="outer"))
print(pd.merge(df3, df4, left_on="lkey", right_on="rkey", how="outer"))
# p 262
"""
При соединении типа многие ко многим строится декартово произведение
соответственных ключей.
"""
df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"],
"data1": pd.Series(range(6), dtype="Int64")})
df2 = pd.DataFrame({"key": ["a", "b", "a", "b", "d"],
"data2": pd.Series(range(5), dtype="Int64")})
print(pd.merge(df1, df2, on="key", how="left"))
print(pd.merge(df1, df2, on="key", how="inner"))
#  p 276
data = pd.DataFrame(np.arange(6).reshape((2, 3)),
index=pd.Index(["Ohio", "Colorado"], name="state"),
columns=pd.Index(["one", "two", "three"],
name="number"))
print(data)
result = data.stack()
print(result)
print(result.unstack())
ph = "McKinney/examples/"
data = pd.read_csv("McKinney/examples/macrodata.csv")
data = data.loc[:, ["year", "quarter", "realgdp", "infl", "unemp"]]
print(data.head())
periods = pd.PeriodIndex(year=data.pop("year"),
quarter=data.pop("quarter"),
name="date")
print(periods)
data.index = periods.to_timestamp("D")
print(data.head())
data = data.reindex(columns=["realgdp", "infl", "unemp"])
data.columns.name = "item"
print(data.head())
long_data = (data.stack()
.reset_index()
.rename(columns={0: "value"}))
print(long_data[:10])
pivoted = long_data.pivot(index="date", columns="item",
values="value")
print(pivoted.head())


