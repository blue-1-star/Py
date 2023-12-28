# p 101  NumPy 
# import numpy as np
# my_arr = np.arange(1_000_000)
# my_list = list(range(1_000_000))
# %timeit my_arr2 = my_arr * 2
import numpy as np
import time

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

