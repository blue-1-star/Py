import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import seaborn as sns
mpg = sns.load_dataset("mpg")
mpg.head()
sns.relplot(x="horsepower", y="acceleration", size="cylinders", data=mpg)
