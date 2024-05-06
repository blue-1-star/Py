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



