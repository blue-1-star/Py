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
str_1_04 = "select empno,ename,deptno,sal from emp"
df_emp1_04 = pd.io.sql.read_sql(str_1_04, connection, index_col='empno')
print(df_emp1_04)
print("attribute access:")
print(df_emp1_04.ename) # attribute access
# print("loc properties:")
print("row extraction by position:")
print(df_emp1_04.iloc[[0,2]]) #   row extraction by position
# print(df_emp1_04.loc['job'])
print("df_emp1_04 index:  ",df_emp1_04.index)
only_first_three = df_emp1_04[:11]
# print(f'only_first_three = {only_first_three}') 
# print("delete rows: 0:12 -> ")
# df_del = df_emp1_04[:12].drop()
df_del = df_emp1_04.drop(df_emp1_04.index[:11])
print("delete rows: 0:12 ->\n",df_del)

# ------------
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
# str_1_13 = "select ename, job, deptno from emp where deptno in (10,20)"
str_1_13 = "select ename, job, deptno from emp where deptno in (10,20) and (ename like '%I%' or job like '%ER%')"
df_emp1_13 = pd.io.sql.read_sql(str_1_13, connection)
print(df_emp1_13)
str_2_01 = "select ename,job,sal from emp \
where deptno = 10 \
order by sal asc"
df_emp2_01 = pd.io.sql.read_sql(str_2_01, connection)
print(df_emp2_01)
str_2_02 = "select empno,deptno,sal,ename,job from emp order by deptno, sal desc"
df_emp2_02 = pd.io.sql.read_sql(str_2_02, connection)
print(df_emp2_02)

