import numpy as np
import pandas as pd
# импортируем библиотеку datetime для работы с датами
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
dir_dat = "G:\\Programming\\Py\\Pandas\\Хейдт\\Data\\"
sensor_data = pd.read_csv(dir_dat + "sensors.csv")
print(sensor_data)
