# p 101  NumPy 
# import numpy as np
# my_arr = np.arange(1_000_000)
# my_list = list(range(1_000_000))
# %timeit my_arr2 = my_arr * 2
import numpy as np
import time
import matplotlib.pyplot as plt
# Создаем массивы
my_arr = np.arange(1_000_000)
my_list = list(range(1_000_000))

# Замеряем время выполнения для NumPy
start_time = time.time()
my_arr2 = my_arr * 2
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Time taken for NumPy operation: {elapsed_time} seconds")

# Замеряем время выполнения для обычного списка
start_time = time.time()
my_list2 = [x * 2 for x in my_list]
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken for list operation: {elapsed_time} seconds")

# p 102
data1 = [6, 7.5, 8, 0, 1]
arr1 = np.array(data1)
print(arr1)
data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)
# p 109
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d)
print(arr2d[2])
print(arr2d[0][2])
print(arr2d[0,2])
lower_dim_slice = arr2d[1, :2]
print(lower_dim_slice)
print(arr2d[:2, 2])
#
# -------------  p 125
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])
result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
print(result)
res_np = np.where(cond, xarr, yarr)
print(f'NumPy->\n{res_np}')
# -------------  p 131
arr = np.arange(10)
arr1 = np.arange(12)
np.save("G:\Programming\Py\McKinney\some_array", arr)
arr_l = np.load("G:\Programming\Py\McKinney\some_array.npy")
print(f'arr load ->  {arr_l}')
np.savez_compressed("G:\Programming\Py\McKinney\\arrays_compressed.npz", a=arr, b=arr1)
arch = np.load("G:\Programming\Py\McKinney\\arrays_compressed.npz")
print(f'arch[a] ->\n{arch["a"]} \narch[b] ->\n{arch["b"]}')

#
#! blockstart
import random
position = 0
walk = [position]
nsteps = 1000
for _ in range(nsteps):
    step = 1 if random.randint(0, 1) else -1    #  random.randint(a, b) returns a random integer N such that a <= N <= b
    position += step
    walk.append(position)
#! blockend
# plt.plot(walk[:100])
# plt.show()

# ------------  p 134 
nsteps = 1000
rng = np.random.default_rng(seed=12345) # Новый генератор случайных чисел
draws = rng.integers(0, 2, size=nsteps)
steps = np.where(draws == 0, 1, -1)
walk = steps.cumsum()
wmin = walk.min()
wmax = walk.max()
print(f'wmin = {wmin}, wmax = {wmax} ')
print(f'argmax= {(np.abs(walk) >= 10).argmax()}')
# ------------  p 134 
import pandas as pd
data = {"state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
"year": [2000, 2001, 2002, 2001, 2002, 2003],
"pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)
print(frame)

# ------------  p 147  Словарь словарей
populations = {"Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
"Nevada": {2001: 2.4, 2002: 2.9}}
frame3 = pd.DataFrame(populations)
print(f'frame3->\n{frame3}')
pdata = {"Ohio": frame3["Ohio"][:-1],
"Nevada": frame3["Nevada"][:2]}
frm = pd.DataFrame(pdata)
print(frm)
# ------------  p 146  
obj1 = pd.Series([1, 2, 3], index=[2, 0, 1])
obj2 = pd.Series([1, 2, 3], index=["a", "b", "c"])
print(obj1)
print(obj2)
print(obj1[[0, 1, 2]])
print(obj2[[0, 1, 2]])
# ------------  p 167
df1 = pd.DataFrame(np.arange(12.).reshape((3, 4)),
columns=list("abcd"))
df2 = pd.DataFrame(np.arange(20.).reshape((4, 5)),
columns=list("abcde"))
df2.loc[1, "b"] = np.nan
print(df1)
print(df2)
print(df1+df2)
print(df1.add(df2, fill_value=0))
print(1/df1)
# ------------  p 167
arr = np.arange(12.).reshape((3, 4))
print(arr)
print(arr - arr[0])
# 169
frame = pd.DataFrame(np.arange(12.).reshape((4, 3)),
columns=list("bde"),
index=["Utah", "Ohio", "Texas", "Oregon"])
series = frame.iloc[0]
print(frame)
print(series)
print(frame - series)
# ------------  p 170
frame = pd.DataFrame(np.random.standard_normal((4, 3)),
columns=list("bde"),
index=["Utah", "Ohio", "Texas", "Oregon"])
print(frame)
def f1(x):
    return x.max() - x.min()
print(np.abs(frame))
print(f'scope ->\n{frame.apply(f1)}')
print(f'axis->\n{frame.apply(f1, axis="columns")}')
def f2(x):
    return pd.Series([x.min(), x.max()], index=["min", "max"])
# frame.apply(f2)
print(frame.apply(f2))
def my_format(x):
    return f"{x:.2f}"
print(frame.applymap(my_format))
# ------------  p 180
import pickle
import pandas  as pd
price = pd.read_pickle("McKinney\yahoo_price.pkl")
volume = pd.read_pickle("McKinney\yahoo_volume.pkl")
print(f'pickle pd \n{price}')
# with open("McKinney/yahoo_price.pkl", 'rb') as file:
    # price1 = pickle.load(file)
# print(f'pickle \n{price1}')
returns = price.pct_change()
print(returns.tail())
print(returns["MSFT"].corr(returns["IBM"]))
print(returns["MSFT"].cov(returns["IBM"]))
print(returns.corr())
print(returns.corrwith(returns["IBM"]))
print(returns.corrwith(volume))













