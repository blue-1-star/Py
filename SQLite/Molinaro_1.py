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
str0= "select * from emp"
df_emp = pd.io.sql.read_sql(str0, connection)
#df_emp = pd.io.sql.read_sql(str0, connection, index_col='empno')
print(df_emp)
# p 41  
str_1_03 = "select * from emp \
    where ( deptno = 10 \
    or comm is not null \
    or sal <= 2000) \
    and deptno=20"
cursor.execute(str_1_03)
results = cursor.fetchall()
print(results)
df_emp1_03 = pd.io.sql.read_sql(str_1_03, connection, index_col='empno')
# print(df_emp1_03)  
#-----------------
# perform the same operation in terms of a dataframe 
# rename  columns and filter 
str_1_06 ="select sal as salary, comm as commission from emp where salary < 3000"
df_emp1_06 = pd.io.sql.read_sql(str_1_06, connection)
print(df_emp1_06)
df_emp_n = df_emp.rename(columns={'sal':'salary','comm':'comission'})
# sc=['salary','comission']
df_emp_n=df_emp_n[['salary','comission']]
print(df_emp_n[df_emp_n.salary < 3000])
# print(df_emp_n)
# ----------------------------------------------------
str_1_07 = "select ename || ' WORKS AS A ' || job as msg  from emp  where deptno=10"
df_emp1_07 = pd.io.sql.read_sql(str_1_07, connection)
print(df_emp1_07)
df_emp1_07d = df_emp.copy()
# add column msg, s1 = ' WORKS AS A ',  ename + s1 + job, apply IF deptno=10, delete all columns except  msg. 
#   GPT
# Создаем новый столбец 'msg' путем конкатенации 'ename' и 'job'
# df_emp1_07['msg'] = df_emp1_07['ename'] + ' WORKS AS A ' + df_emp1_07['job']
df_emp1_07d['msg'] = df_emp['ename'] + ' WORKS AS A ' + df_emp['job']
# Применяем условие, оставляем только строки, где 'deptno' равен 10, и столбец 'msg'
df_emp1_07d = df_emp1_07d[df_emp1_07d['deptno'] == 10][['msg']] 
# print(df_emp['deptno'] == 10)
print(df_emp1_07d)
#
# ----------------------------------------------------

# df_emp = pd.io.sql.read_sql(str0, connection, index_col='empno')
str_1_08 = "select ename,sal,  \
    case when sal <= 2000 then 'UNDERPAID' \
         when sal >= 4000 then 'OVERPAID' \
         else 'OK' \
    end as status \
 from emp"
df_emp1_08 = pd.io.sql.read_sql(str_1_08, connection)

# df_emp 
# df_emp['status'] 
# df_emp[df_emp['sal']<=2000], df_emp[df_emp['sal']>=4000]     

#  GPT 
# Определение условной логики для нового столбца 'status'
def get_status(row):
    if row['sal'] <= 2000:
        return 'UNDERPAID'
    elif row['sal'] >= 4000:
        return 'OVERPAID'
    else:
        return 'OK'
# df_emp['status'] = df_emp.apply(lambda row: get_status(row), axis=1)
print("-----------------  1.08---------------------------")
df_emp1_08d = df_emp.copy()
df_emp1_08d['status'] = df_emp.apply(lambda row: get_status(row), axis=1)
print(df_emp1_08d)
# ----------------------------------------------------
# str_1_09 = 'select * from emp fetch first 5 rows only'   DB2  
str_1_09 = 'select * from emp limit 5'   #  Для СУБД MySQL  PostgreSQL  SQLite
df_emp1_09 = pd.io.sql.read_sql(str_1_09, connection)
print("-----------------  1.09  ---------------------------")
print(df_emp1_09)
df_emp1_09d = df_emp[0:5]
print(df_emp1_09d)
# ----------------------------------------------------
print("-----------------  1.10  ---------------------------")
str_1_10='select ename,job from emp  order by random() limit 5'
df_emp1_10 = pd.io.sql.read_sql(str_1_10, connection)
df_emp1_10d = df_emp[['ename','job']]
print(df_emp1_10)
# print(df_emp1_10d.sample(5))
df_emp1_10d = df_emp1_10d.reset_index(drop=True)
print(df_emp1_10d.sample(5))
# ----------------------------------------------------
print("-----------------  1.11  ---------------------------")
str_1_11 = 'select * from emp where comm is null '
df_emp1_11 = pd.io.sql.read_sql(str_1_11, connection)
print(df_emp1_11)
df_emp1_11d = df_emp[df_emp['comm'].isnull()] 
print(df_emp1_11d)
# ----------------------------------------------------
print("-----------------  1.12  ---------------------------")
str_1_12 = "select coalesce(comm,0) from emp"
df_emp1_12 = pd.io.sql.read_sql(str_1_12, connection)
print(df_emp1_12)
# def null_to_0(row):
#     if row['comm'].isnull():
#         # row['comm']=0
#         return 0        
# GPT version 
def null_to_0(value):
    if pd.isnull(value):  # Проверяем, является ли значение None или NaN
        return 0
    else:
        return value
# df_emp1_12d = df_emp.apply(lambda row: null_to_0(row), axis=1)
# df_emp1_12d = df_emp.apply(lambda col: col.apply(null_to_0))
df_emp1_12d = df_emp['comm'].apply(null_to_0)
# print(df_emp1_12d[['comm']])
print(df_emp1_12d)
# print(df_emp1_12d.info())
print("-----------------  1.13  ---------------------------")
str_1_13 = "select ename, job from emp where deptno in (10,20)"
df_emp1_13 = pd.io.sql.read_sql(str_1_13, connection)
# print(df_emp1_13)
# df_emp1_13d = df_emp[(df_emp['deptno'] == 10) | (df_emp['deptno'] == 20)]
# df_emp1_13d = df_emp1_13d.reset_index(drop=True)  # Сброс индексов
str_1_13a = "select ename, job  from emp  where deptno in (10, 20) and (ename like '%I%' or job like '%ER%')"
df_emp1_13a = pd.io.sql.read_sql(str_1_13a, connection)
print(df_emp1_13a)
# df_emp1_13ad = df_emp[(df_emp['deptno'] == 10) | (df_emp['deptno'] == 20) & (('I' in df_emp['ename']) | ('ER' in df_emp['job'])) ]
# df_emp1_13ad = df_emp[((df_emp['deptno'] == 10) | (df_emp['deptno'] == 20)) & (('I' in df_emp['ename']) | ('ER' in df_emp['job']))]
# df_emp1_13ad = df_emp[((df_emp['deptno'] == 10) | (df_emp['deptno'] == 20)) & (df_emp['ename'].str.contains('I') | df_emp['job'].str.contains('ER'))]
# print(df_emp1_13a)
conditions = ((df_emp['deptno'].isin([10, 20])) & (df_emp['ename'].str.contains('I') | df_emp['job'].str.contains('ER')))
df_emp1_13ad = df_emp[conditions]
df_emp1_13ad = df_emp1_13ad.reset_index(drop=True)  # Сброс индексов
# print(df_emp1_13ad)
print(df_emp1_13ad[['ename','job']])
# 'I' in ename  or 'ER' in job














