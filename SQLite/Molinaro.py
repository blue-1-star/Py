"""
Энтони Молинаро Роберт де Грааф Сборник рецептов   Санкт-Петербург « БХВ-Петербург»
2022 2-е издание
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
# p 41  
str_1_03 = "select * from emp \
    where ( deptno = 10 \
    or comm is not null \
    or sal <= 2000) \
    and deptno=20"
cursor.execute(str_1_03)
results = cursor.fetchall()
print(results)
df_emp = pd.io.sql.read_sql(str_1_03, connection, index_col='empno')
print(df_emp)  
str_1_04 = "select ename,deptno,sal from emp"
df_emp1_04 = pd.io.sql.read_sql(str_1_04, connection)
print(df_emp1_04)
str_1_05 ="select sal as salary, comm as commission from emp"
df_emp1_05 = pd.io.sql.read_sql(str_1_05, connection)
print(df_emp1_05)
str_1_06 ="select sal as salary, comm as commission from emp where salary < 3000"
df_emp1_06 = pd.io.sql.read_sql(str_1_06, connection)
print(df_emp1_06)
# str_1_07 = "select ename, job from emp where deptno = 10"
str_1_07 = "select ename || ' WORKS AS A ' || job as msg  from emp  where deptno=10"
df_emp1_07 = pd.io.sql.read_sql(str_1_07, connection)
print(df_emp1_07)
str_1_08 = "select ename,sal,  \
    case when sal <= 2000 then 'UNDERPAID' \
         when sal >= 4000 then 'OVERPAID' \
         else 'OK' \
    end as status \
 from emp"
df_emp1_08 = pd.io.sql.read_sql(str_1_08, connection)
print(df_emp1_08)
str_1_11 = "select * from emp  where comm is null"
df_emp1_11 = pd.io.sql.read_sql(str_1_11, connection)
print(df_emp1_11)
str_1_12 = "select coalesce(comm,0) from emp"
df_emp1_12 = pd.io.sql.read_sql(str_1_12, connection)
print(df_emp1_12)



