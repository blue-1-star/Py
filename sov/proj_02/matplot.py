import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
# plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])

x = np.linspace(0, 10, 50)
y=x
# plt.title('Линейная зависимость y = x')
# plt.plot(x, y,'r--')
plt.xlabel('x') # ось абсцисс
plt.ylabel('y') # ось ординат
plt.grid()
y1 = x
y2 = [i**2 for i in x]
plt.title('Зависимости: y1 = x, y2 = x^2')
plt.ylabel('y1, y2')
plt.plot(x, y1, x, y2)

plt.figure(figsize=(9, 9))
plt.subplot(2, 1, 1)
plt.plot(x, y1)
plt.title('Зависимости: y1 = x, y2 = x^2')
plt.ylabel('y1', fontsize=14)
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(x, y2)
plt.xlabel('x', fontsize=14)
plt.ylabel('y2', fontsize=14)
plt.grid(True)

fruits = ['apple', 'peach', 'orange', 'bannana', 'melon']
counts = [34, 25, 43, 31, 17]
plt.bar(fruits, counts)
plt.title('Fruits!')
plt.xlabel('Fruit')
plt.ylabel('Count')
plt.show()

