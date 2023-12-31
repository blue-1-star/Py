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




