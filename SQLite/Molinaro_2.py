"""
Энтони Молинаро Роберт де Грааф Сборник рецептов   Санкт-Петербург « БХВ-Петербург»
2022 2-е издание
Глава 2
"""
import sqlite3
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
pa='G:\\Programming\\Py\\SQLite\\Data\\'
fi = "my_dbase.db"
pafi = pa + fi
connection = sqlite3.connect(pafi)
cursor = connection.cursor()
str0= "select * from emp"
df_emp = pd.io.sql.read_sql(str0, connection)
str_2_01 = 'select ename,job,sal from emp where deptno = 10 order by sal asc'
cursor.execute(str_2_01)
df_emp2_01 = pd.io.sql.read_sql(str_2_01, connection)
print(df_emp2_01)
