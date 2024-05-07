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
    iris = sns.load_dataset("iris")
    print(iris.head())
    sns.catplot(x="species", y="sepal_length", kind="swarm", data=iris)
    plt.show()        


