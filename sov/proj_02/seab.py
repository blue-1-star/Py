import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import seaborn as sns
def f_6_2_1():
    # 6.2.1 Построение точечного графика  p  124
    # file_data =r"G:\Programming\Py\sov\proj_02\data_learn\auto_mpg_dataset.csv"
    # mpg = pd.read_csv(file_data)
    # mpg = sns.load_dataset(file_data)
    mpg = sns.load_dataset("mpg")
    
    print(mpg.head())
    sns.relplot(x="horsepower", y="acceleration", size="cylinders", data=mpg)
    plt.show()        
def f_6_2_2():
    # 6.2.2 Построение линейного графика  p  125
    flights = sns.load_dataset("flights")
    print(flights.head())
    sns.relplot(x="year", y="passengers", kind="line", legend="full",
    data=flights)
    plt.show()        
def f_6_2_3():
    # 6.2.3 Работа с категориальными данными p  126
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    iris = sns.load_dataset("iris")
    # sns.catplot(x="species", y="sepal_length", kind="swarm", data=iris, ax=axes[0])
    sns.swarmplot(x="species", y="sepal_length", data=iris, ax=axes[0])
    sns.boxplot(x="species", y="sepal_length", data=iris, ax=axes[1])
    plt.show()
def f_7_1():
    # 6.2.3 Работа с категориальными данными p  126
    # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    flights = sns.load_dataset("flights")
    # sns.set_style("darkgrid")
    # sns.set_style("whitegrid")
    sns.set_style("dark")
    sns.lineplot(x='year', y='passengers', data=flights)
    plt.show()   
def f_7_3_1():
    # 7.3.1 Сетка  p 139
    # sns.set_style("whitegrid")
    # sns.set_context("notebook")
    sns.set_style("whitegrid", rc={'grid.color': '#ff0000', 'grid.linestyle': '--'})
    sns.set_context("notebook", rc={'grid.linewidth': 3.0})
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 5))
    iris = sns.load_dataset("iris")
    # sns.catplot(x="species", y="sepal_length", kind="swarm", data=iris, ax=axes[0])
    sns.swarmplot(x="species", y="sepal_length", data=iris, ax=axes[0])
    sns.boxplot(x="species", y="sepal_length", data=iris, ax=axes[1])
    sns.scatterplot(x='sepal_length', y='petal_length', data=iris, ax = axes[2])
    plt.show()         

def f_8_2_1():
    # 8.2.1 Знакомство с функцией lineplot() p 157
    sns.set_style("darkgrid")
    # sns.set_context("notebook")
    fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(12, 5))
    np.random.seed(123)
    x = [i for i in range(10)]
    sample = [i for i in range(10)]
    y = np.random.randint(10, size=len(x))
    z = np.random.randint(4, size=len(sample))
    data = [sample, y, z]
    df = pd.DataFrame(data).transpose()
    df.columns = ['sample', 'y_val', 'z_val']
    # sns.lineplot(x='sample', y='y_val', data = df)
    sns.lineplot(data=df, ax = axes[0])
    sns.lineplot(x=df['z_val'], y=df['y_val'], ax =axes[1])
    # sns.lineplot(x=df['z_val'], y=df['y_val'], ax =axes[2], ci = 'sd')

    # print(df)
    # 8.2.3 Повышение информативности графика
    df_m = sns.load_dataset("mpg")
    # print(df_m.head())
    # dir_dat = r"G:\Programming\Py\sov\proj_02\data_learn\auto_mpg_dataset_.xlsx"
    # df_m.to_excel(dir_dat)
    sns.set_style("darkgrid")
    # sns.lineplot(x='model_year', y='horsepower', data=df_m, ax=axes[2])
    # отдельно для стран США и Японии  параметр hue для выделения стран цветом:
    sns.lineplot(x='model_year', y='horsepower', hue='origin',
    data=df_m[df_m['origin'] != 'europe'], ax=axes[2])
    df_usa_jp = df_m[df_m['origin'] != 'europe']
    # palette, hue_order, hue_norm
    sns.lineplot(x='model_year', y='horsepower', hue='origin',
    palette={'usa':'r', 'japan':'b'}, hue_order=['japan', 'usa'],
    data=df_usa_jp, ax=axes[3])
    plt.show()         
def f_8_2_1a():
    # 8.2.1 Знакомство с функцией lineplot() p 157
    sns.set_style("darkgrid")
    # sns.set_context("notebook")
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 5))
    np.random.seed(123)
    x = [i for i in range(10)]
    sample = [i for i in range(10)]
    y = np.random.randint(10, size=len(x))
    z = np.random.randint(4, size=len(sample))
    data = [sample, y, z]
    df = pd.DataFrame(data).transpose()
    df.columns = ['sample', 'y_val', 'z_val']
    # sns.lineplot(x='sample', y='y_val', data = df)
    sns.lineplot(data=df, ax = axes[0,0])
    sns.lineplot(x=df['z_val'], y=df['y_val'], ax =axes[0,1])
    # sns.lineplot(x=df['z_val'], y=df['y_val'], ax =axes[2], ci = 'sd')

    # print(df)
    # 8.2.3 Повышение информативности графика
    df_m = sns.load_dataset("mpg")
    # print(df_m.head())
    # dir_dat = r"G:\Programming\Py\sov\proj_02\data_learn\auto_mpg_dataset_.xlsx"
    # df_m.to_excel(dir_dat)
    sns.set_style("darkgrid")
    # sns.lineplot(x='model_year', y='horsepower', data=df_m, ax=axes[2])
    # отдельно для стран США и Японии  параметр hue для выделения стран цветом:
    sns.lineplot(x='model_year', y='horsepower', hue='origin',
    data=df_m[df_m['origin'] != 'europe'], ax=axes[0,2])
    df_usa_jp = df_m[df_m['origin'] != 'europe']
    # palette, hue_order, hue_norm
    sns.lineplot(x='model_year', y='horsepower', hue='origin',
    palette={'usa':'r', 'japan':'b'}, hue_order=['japan', 'usa'],
    data=df_usa_jp, ax=axes[1,0])
    sns.lineplot(x='model_year', y='horsepower', style='origin',
    dashes={'usa': (2, 2), 'japan': (5, 2)}, data=df_usa_jp, ax=axes[1,1])
    sns.lineplot(x='model_year', y='horsepower', style='origin',
    dashes=False, markers={'usa': '^', 'japan': 'o'}, data=df_usa_jp, ax=axes[1,2])
    #  p 168 
    # 8.2.3.3 Настройка толщины линии
    fn_filter = lambda x: True if x in [4, 8] else False
    fn_mod = lambda x: {4: 'four', 8: 'eight'}[x]
    df_mod1 = df_m[df_m['cylinders'].map(fn_filter)].copy()
    df_mod1['cylinders'] = df_mod1['cylinders'].map(fn_mod)
    sns.lineplot(x='model_year', y='horsepower', size='cylinders',
    data=df_mod1, ax=axes[1,3])
    plt.tight_layout()
    plt.show()   

def f_8_3():
    # 8.3 Диаграмма рассеяния. Функция scatterplot() p 171
    sns.set_style("darkgrid")
    df = sns.load_dataset("iris")
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 5))
    # sns.catplot(x="species", y="sepal_length", kind="swarm", data=iris, ax=axes[0])
    sns.scatterplot(x='sepal_length', y='petal_length', data=df, ax = axes[0,0])
    mpg = sns.load_dataset("mpg")
    sns.scatterplot(x='mpg', y='displacement', data=mpg, ax = axes[0,1])
    sns.scatterplot(x='mpg', y='displacement', hue='origin', data=mpg, ax = axes[0,2])
    sns.scatterplot(x='mpg', y='displacement', hue='origin',
    palette='plasma', data=mpg, ax= axes[0,3])
    plt.tight_layout()
    plt.show()         

def f_8_5():
    # 8.5 Визуализация отношений с настройкой подложки. Функция relplot() p 185
    sns.set_style("whitegrid")
    iris = sns.load_dataset("iris")
    # fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(12, 5))
    # sns.catplot(x="species", y="sepal_length", kind="swarm", data=iris, ax=axes[0])
    sns.relplot(x='sepal_length', y='petal_length', data=iris, kind ='scatter')
    # sns.scatterplot(x='sepal_length', y='petal_length', data=iris, ax=axes[0, 0])
    plt.tight_layout()
    plt.show()         
