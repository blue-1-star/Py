"""
Python. Визуализация данных. Matplotlib. Seaborn. Mayavi
© Абдрахманов М.И., 2020
"""

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
import matplotlib.gridspec as gridspec
# plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])

def f_1_03():
    # 1.4 Несколько графиков на одном поле 

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
    plt.show()

def f_1_04():
    # 1.5 Представление графиков на разных полях
    x = np.linspace(0, 10, 50)
    y1 = x
    y2 = [i**2 for i in x]
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
    plt.show()

def f_1_05():
    fruits = ['apple', 'peach', 'orange', 'bannana', 'melon']
    counts = [34, 25, 43, 31, 17]
    plt.bar(fruits, counts)
    plt.title('Fruits!')
    plt.xlabel('Fruit')
    plt.ylabel('Count')
    plt.show()

def f_1_06():
    import matplotlib.pyplot as plt
    from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
    AutoMinorLocator)
    import numpy as np
    x = np.linspace(0, 10, 10)
    y1 = 4*x
    y2 = [i**2 for i in x]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title('Графики зависимостей: y1=4*x, y2=x^2', fontsize=16)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y1, y2', fontsize=14)
    ax.grid(which='major', linewidth=1.2)
    ax.grid(which='minor', linestyle='--', color='gray', linewidth=0.5)
    ax.scatter(x, y1, c='red', label='y1 = 4*x')
    ax.plot(x, y2, label='y2 = x^2')
    ax.legend()
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='major', length=10, width=2)
    ax.tick_params(which='minor', length=5, width=1)
    x = [1, 5, 10, 15, 20]
    y = [1, 7, 3, 5, 11]
    plt.plot(x, y, label='steel price')
    plt.title('Chart price', fontsize=15)
    plt.xlabel('Day', fontsize=12, color='blue')
    plt.ylabel('Price', fontsize=12, color='blue')
    plt.legend()
    plt.grid(True)
    plt.text(15, 4, 'grow up!')
    plt.show()

# def f_2_4_1():
def f_1_07():
    # 2.4 Размещение графиков отдельно друг от  друга
    # p 30 -31
    x = [1, 5, 10, 15, 20]
    y1 = [1, 7, 3, 5, 11]
    y2 = [i*1.2 + 1 for i in y1]
    y3 = [i*1.2 + 1 for i in y2]
    y4 = [i*1.2 + 1 for i in y3]
    # plt.figure(figsize=(12, 7))
    plt.figure(figsize=(18, 11))
    plt.subplot(2, 2, 1)
    plt.plot(x, y1, '-')
    plt.subplot(2, 2, 2)
    plt.plot(x, y2, '--')
    plt.subplot(2, 2, 3)
    plt.plot(x, y3, '-.')
    plt.subplot(2, 2, 4)
    plt.plot(x, y4, ':')
    plt.show()

def f_2_4_2():
    # p 33 
    # 2.4.2 Работа с функцией subplots()
    x = [1, 5, 10, 15, 20]
    y1 = [1, 7, 3, 5, 11]
    y2 = [i*1.2 + 1 for i in y1]
    y3 = [i*1.2 + 1 for i in y2]
    y4 = [i*1.2 + 1 for i in y3]
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    axs[0, 0].plot(x, y1, '-')
    axs[0, 1].plot(x, y2, '--')
    axs[1, 0].plot(x, y3, '-.')
    axs[1, 1].plot(x, y4, ':')
    plt.show()

def f_3_2_1():
    # 3.2.1 Инструмент GridSpec
    x = [1, 2, 3, 4, 5]
    y1 = [9, 4, 2, 4, 9]
    y2 = [1, 7, 6, 3, 5]
    fg = plt.figure(figsize=(7, 3), constrained_layout=True)
    gs = gridspec.GridSpec(ncols=2, nrows=1, figure=fg)
    fig_ax_1 = fg.add_subplot(gs[0, 0])
    plt.plot(x, y1)
    fig_ax_2 = fg.add_subplot(gs[0, 1])
    plt.plot(x, y2)
    plt.show()

