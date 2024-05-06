"""
Python. Визуализация данных. Matplotlib. Seaborn. Mayavi
© Абдрахманов М.И., 2020
"""

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
bc = mcolors.BASE_COLORS
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

def f_3_2_1a():
    # 3.2.1 Инструмент GridSpec  new layout
    x = [1, 2, 3, 4, 5]
    y1 = [9, 4, 2, 4, 9]
    y2 = [1, 7, 6, 3, 5]
    y3 = [-7, -4, 2, -4, -7]
    fg = plt.figure(figsize=(9, 4), constrained_layout=True)
    gs = fg.add_gridspec(2, 2)
    fig_ax_1 = fg.add_subplot(gs[0, :])
    plt.plot(x, y2)
    fig_ax_2 = fg.add_subplot(gs[1, 0])
    plt.plot(x, y1)
    fig_ax_3 = fg.add_subplot(gs[1, 1])
    plt.plot(x, y3)
    plt.show()
def f_3_9():
    fg = plt.figure(figsize=(9, 9), constrained_layout=True)
    gs = fg.add_gridspec(5, 5)
    fig_ax_1 = fg.add_subplot(gs[0, :3])
    fig_ax_1.set_title('gs[0, :3]')
    fig_ax_2 = fg.add_subplot(gs[0, 3:])
    fig_ax_2.set_title('gs[0, 3:]')
    fig_ax_3 = fg.add_subplot(gs[1:, 0])
    fig_ax_3.set_title('gs[1:, 0]')
    fig_ax_4 = fg.add_subplot(gs[1:, 1])
    fig_ax_4.set_title('gs[1:, 1]')
    fig_ax_5 = fg.add_subplot(gs[1, 2:])
    fig_ax_5.set_title('gs[1, 2:]')
    fig_ax_6 = fg.add_subplot(gs[2:4, 2])
    fig_ax_6.set_title('gs[2:4, 2]')
    fig_ax_7 = fg.add_subplot(gs[2:4, 3:])
    fig_ax_7.set_title('gs[2:4, 3:]')
    fig_ax_8 = fg.add_subplot(gs[4, 3:])
    fig_ax_8.set_title('gs[4, 3:]')
    plt.show()
def f_3_11():
    # 3.3 Текстовые элементы графика
    plt.figure(figsize=(10,4))
    plt.figtext(0.5, -0.1, 'figtext')
    plt.suptitle('suptitle')
    plt.subplot(121)
    plt.title('title')
    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.text(0.2, 0.2, 'text')
    plt.annotate('annotate', xy=(0.2, 0.4), xytext=(0.6, 0.7),
    arrowprops=dict(facecolor='black', shrink=0.05))
    plt.subplot(122)
    plt.title('title')
    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.text(0.5, 0.5, 'text')
    plt.show()
def f_3_3_1():
    # 3.3.1 Заголовок фигуры и поля графика
    weight=['light', 'regular', 'bold']
    plt.figure(figsize=(12, 4))
    plt.subplots_adjust(top=0.85-0.1)
    for i, lc in enumerate(['left', 'center', 'right']):
        plt.subplot(1, 3, i+1)
        plt.title(label=lc, loc=lc, fontsize=12+i*5, fontweight=weight[i],
        pad=10+i*15)
    plt.show()

def f_3_3_2():
    # 3.3.2 Подписи осей графика
    plt.figure(figsize=(7, 7))
    x = [i for i in range(10)]
    y = [i*2 for i in range(10)]
    plt.plot(x, y)
    # plt.xlabel('Ось X')
    # plt.ylabel('Ось Y')
    plt.xlabel('Ось X\nНезависимая величина', fontsize=14, fontweight='bold')
    plt.ylabel('Ось Y\nЗависимая величина', fontsize=14, fontweight='bold')
    plt.show()

def f_3_3_3():
    # 3.3.3 Текстовый блок
    # plt.figure(figsize=(7, 7))
    bbox_properties=dict(boxstyle='darrow, pad=0.3', ec='k', fc='y', ls='-',
    lw=3)
    plt.text(2, 7, 'HELLO!', fontsize=15, bbox=bbox_properties)
    # plt.text(0, 7, 'HELLO!', fontsize=15)
    plt.plot(range(0,10), range(0,10))
    plt.show()

def f_4_1():
    # Линейный график p 77
    # plt.figure(figsize=(7, 7))
    x = [1, 5, 10, 15, 20]
    y1 = [1, 7, 3, 5, 11]
    y2 = [4, 3, 1, 8, 12]
    plt.figure(figsize=(12, 7))
    plt.plot(x, y1, 'o-r', alpha=0.7, label='first', lw=5, mec='b', mew=2,
    ms=10)
    plt.plot(x, y2, 'v-.g', label='second', mec='r', lw=2, mew=2, ms=12)
    plt.legend()
    plt.grid(True)
    plt.show()
def f_4_2():
    # график с заливкой: p 78
    # plt.figure(figsize=(7, 7))
    x = np.arange(0.0, 5, 0.01)
    y = np.cos(x*np.pi)
    plt.plot(x, y, c = 'r')
    # plt.fill_between(x, y)
    # plt.fill_between(x, y, where = (y > 0.75) | (y < -0.75))
    plt.fill_between(x, y, where=y>=0, color='g', alpha=0.3)
    plt.fill_between(x, y, where=y<=0, color='r', alpha=0.3)
    plt.show()
def f_4_3():
    # график с заливкой: p 78
    np.random.seed(123)
    groups = [f'P{i}' for i in range(7)]
    counts = np.random.randint(3, 10, len(groups))
    plt.bar(groups, counts)
    plt.show()    

def f_4_3_1():
    # Пример, демонстрирующий работу с параметрами bar(): p  98
    np.random.seed(123)
    groups = [f'P{i}' for i in range(7)]
    counts = np.random.randint(0, len(bc), len(groups))
    width = counts*0.1
    colors = [['r', 'b', 'g'][int(np.random.randint(0, 3, 1))] for _ in
    counts]
    plt.bar(groups, counts, width=width, alpha=0.6, bottom=2, color=colors,
    edgecolor='k', linewidth=2)
    plt.show()    
def f_4_3_1_1():
    # Пример, демонстрирующий работу с параметрами bar(): p  98
    cat_par = [f'P{i}' for i in range(5)]
    g1 = [10, 21, 34, 12, 27]
    g2 = [17, 15, 25, 21, 26]
    width = 0.3
    x = np.arange(len(cat_par))
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, g1, width, label='g1')
    rects2 = ax.bar(x + width/2, g2, width, label='g2')
    ax.set_title('Пример групповой диаграммы')
    ax.set_xticks(x)
    ax.set_xticklabels(cat_par)
    ax.legend()
    plt.show()        

def f_4_3_1_2():
    # 4.3.1.2 Диаграмма с errorbar-элементом p  99
    np.random.seed(123)
    rnd = np.random.randint
    cat_par = [f'P{i}' for i in range(5)]
    g1 = [10, 21, 34, 12, 27]
    error = np.array([[rnd(2,7),rnd(2,7)] for _ in range(len(cat_par))]).T
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].bar(cat_par, g1, yerr=5, ecolor='r', alpha=0.5, edgecolor='b',
    linewidth=2)
    axs[1].bar(cat_par, g1, yerr=error, ecolor='r', alpha=0.5, edgecolor='b',
    linewidth=2)
    plt.show()        
def f_4_3_2_1():
    # 4.3.2.1 Классическая круговая диаграмма  p  100
    vals = [24, 17, 53, 21, 35]
    labels = ['Ford', 'Toyota', 'BMW', 'AUDI', 'Jaguar']
    explode = [0, 0, 0.1, 0, 0]
    fig, ax = plt.subplots()
    ax.pie(vals, labels=labels,  explode=explode, autopct='%1.1f%%', shadow=True)
    ax.axis('equal')
    plt.show()        
def f_4_3_2_2():
    # 4.3.2.2 Вложенные круговые диаграммы  p  104
    fig, ax = plt.subplots()
    offset=0.4
    data = np.array([[5, 10, 7], [8, 15, 5], [11, 9, 7]])
    cmap = plt.get_cmap('tab20b')
    b_colors = cmap(np.array([0, 8, 12]))
    sm_colors = cmap(np.array([1, 2, 3, 9, 10, 11, 13, 14, 15]))
    ax.pie(data.sum(axis=1), radius=1, colors=b_colors,
    wedgeprops=dict(width=offset, edgecolor='w'))
    ax.pie(data.flatten(), radius=1-offset, colors=sm_colors,
    wedgeprops=dict(width=offset, edgecolor='w'))
    plt.show()        
