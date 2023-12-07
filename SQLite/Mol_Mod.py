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
def f_1_03():
    print("-----------------  1.03---------------------------")
    str_1_03 = "select * from emp \
        where ( deptno = 10 \
        or comm is not null \
        or sal <= 2000) \
        and deptno=20"
    df_emp1_03 = pd.io.sql.read_sql(str_1_03, connection)
    print(df_emp1_03)
    df_emp1_03d = df_emp[((df_emp['deptno'] == 10) | (~df_emp['comm'].isnull()) | (df_emp['sal'] <= 2000)) & (df_emp['deptno'] == 20)]
    first_part = (df_emp['deptno'] == 10) | (~df_emp['comm'].isnull()) | (df_emp['sal'] <= 2000)
    sec_part = (df_emp['deptno'] == 20)
    df_emp1_03d = df_emp[first_part & sec_part]
    print("dataFrame___")
    print(df_emp1_03d)                  
def f_1_04():
    # print('--- 1.02 ---')   
    print("-----------------  1.04---------------------------")
    str1_04 = 'select ename,deptno,sal from emp'
    df_emp1_04 = pd.io.sql.read_sql(str1_04, connection)
    print(df_emp1_04)
    df_emp_1_04d=df_emp[['ename','deptno','sal']]
    print(df_emp_1_04d)   
def f_1_05():
    print("-----------------  1.05---------------------------")
    str1_05 = 'select sal as salary, comm as commission from emp where salary < 5000'
    df_emp1_05 = pd.io.sql.read_sql(str1_05, connection)
    print('count->',df_emp1_05.count(),"\n")
    print(df_emp1_05)
    # df_emp_1_04d = df_emp.rename(columns={'sal':'salary','comm':'comission'})
    # df_emp_1_04d = pd.io.sql.read_sql(str1_04, connection).rename(columns={'sal':'salary','comm':'comission'})
    print('Frame ->')
    df_emp_1_05d = df_emp[['sal', 'comm']].rename(columns={'sal': 'salary', 'comm': 'commission'})
    # print()
    print(df_emp_1_05d[df_emp_1_05d.salary < 5000])
    print(f'count= {df_emp_1_05d[df_emp_1_05d.salary < 5000].count()}')
def f_1_06():
    print("-----------------  1.06---------------------------")
    str_1_06 ="select sal as salary, comm as commission from emp where salary < 3000"
    df_emp1_06 = pd.io.sql.read_sql(str_1_06, connection)
    print(df_emp1_06)
    df_emp_n = df_emp.rename(columns={'sal':'salary','comm':'comission'})
    # sc=['salary','comission']
    df_emp_n=df_emp_n[['salary','comission']]
    print(df_emp_n[df_emp_n.salary < 3000])
    # print(df_emp_n)
def f_1_07():
    print("-----------------  1.07---------------------------")
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
def f_1_08():
    print("-----------------  1.08---------------------------")
    str_1_08 = "select ename,sal,  \
    case when sal <= 2000 then 'UNDERPAID' \
         when sal >= 4000 then 'OVERPAID' \
         else 'OK' \
    end as status \
    from emp"
    df_emp1_08 = pd.io.sql.read_sql(str_1_08, connection)
    print('SQL ->')
    print(df_emp1_08)
#  GPT 
# Определение условной логики для нового столбца 'status'
    def get_status(row):
        if row['sal'] <= 2000:
            return 'UNDERPAID'
        elif row['sal'] >= 4000:
            return 'OVERPAID'
        else:
            return 'OK'
        # axis {0 or ‘index’, 1 or ‘columns’}”, default 0
    df_emp1_08d = df_emp.copy()
    df_emp1_08d['status'] = df_emp.apply(lambda row: get_status(row), axis=1)
    print("dataFrame___")
    print(df_emp1_08d)
def f_1_09():
    print("-----------------  1.09  ---------------------------")
    # str_1_09 = 'select * from emp fetch first 5 rows only'   DB2  
    str_1_09 = 'select * from emp limit 5'   #  Для СУБД MySQL  PostgreSQL  SQLite
    df_emp1_09 = pd.io.sql.read_sql(str_1_09, connection)
    print('SQL ->')
    print(df_emp1_09)
    df_emp1_09d = df_emp[0:5]
    print("dataFrame->")
    print(df_emp1_09d)
