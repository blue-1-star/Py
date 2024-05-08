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
    np.random.seed(123)
    x = [i for i in range(10)]
    sample = [i for i in range(10)]
    y = np.random.randint(10, size=len(x))
    z = np.random.randint(4, size=len(sample))
    data = [sample, y, z]
    df = pd.DataFrame(data).transpose()
    df.columns = ['sample', 'y_val', 'z_val']
    sns.lineplot(x=x, y=y)
    plt.show()         

