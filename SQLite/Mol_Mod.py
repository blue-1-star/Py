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
    print("dataFrame->\n",df_emp1_09d)
def f_1_10():
    print("-----------------  1.10  ---------------------------")
    str_1_10='select ename,job from emp  order by random() limit 5'
    df_emp1_10 = pd.io.sql.read_sql(str_1_10, connection)
    df_emp1_10d = df_emp[['ename','job']]
    print('SQL ->\n',df_emp1_10)
    # print(df_emp1_10d.sample(5))
    df_emp1_10d = df_emp1_10d.reset_index(drop=True)
    print("dataFrame->\n",df_emp1_10d.sample(5))
def f_1_11():
    print("-----------------  1.11  ---------------------------")
    str_1_11 = 'select * from emp where comm is null '
    df_emp1_11 = pd.io.sql.read_sql(str_1_11, connection)
    print('SQL ->\n',df_emp1_11)
    df_emp1_11d = df_emp[df_emp['comm'].isnull()] 
    print("dataFrame->\n",df_emp1_11d)  
def f_1_12():
    print("-----------------  1.12  ---------------------------")
    str_1_12 = "select coalesce(comm,0) from emp"
    df_emp1_12 = pd.io.sql.read_sql(str_1_12, connection)
    print('SQL ->\n',df_emp1_12)
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
    print("dataFrame->\n",df_emp1_12d)
    # print(df_emp1_12d.info())
def f_1_13():
    print("-----------------  1.13  ---------------------------")
    str_1_13 = "select ename, job from emp where deptno in (10,20)"
    df_emp1_13 = pd.io.sql.read_sql(str_1_13, connection)
    # print(df_emp1_13)
    # df_emp1_13d = df_emp[(df_emp['deptno'] == 10) | (df_emp['deptno'] == 20)]
    # df_emp1_13d = df_emp1_13d.reset_index(drop=True)  # Сброс индексов
    str_1_13a = "select ename, job  from emp  where deptno in (10, 20) and (ename like '%I%' or job like '%ER%')"
    df_emp1_13a = pd.io.sql.read_sql(str_1_13a, connection)
    print('SQL ->\n',df_emp1_13a)
    # df_emp1_13ad = df_emp[(df_emp['deptno'] == 10) | (df_emp['deptno'] == 20) & (('I' in df_emp['ename']) | ('ER' in df_emp['job'])) ]
    # df_emp1_13ad = df_emp[((df_emp['deptno'] == 10) | (df_emp['deptno'] == 20)) & (('I' in df_emp['ename']) | ('ER' in df_emp['job']))]
    # df_emp1_13ad = df_emp[((df_emp['deptno'] == 10) | (df_emp['deptno'] == 20)) & (df_emp['ename'].str.contains('I') | df_emp['job'].str.contains('ER'))]
    # print(df_emp1_13a)
    conditions = ((df_emp['deptno'].isin([10, 20])) & (df_emp['ename'].str.contains('I') | df_emp['job'].str.contains('ER')))
    df_emp1_13ad = df_emp[conditions]
    df_emp1_13ad = df_emp1_13ad.reset_index(drop=True)  # Сброс индексов
    # print(df_emp1_13ad)
    print("dataFrame->\n",df_emp1_13ad[['ename','job']])
    # 'I' in ename  or 'ER' in job
def f_2_01():
    str_2_01 = "select  ename,job,sal  from emp  where deptno = 10  order by sal asc"    
    df_emp2_01 = pd.io.sql.read_sql(str_2_01, connection)
    print('SQL ->\n',df_emp2_01)
    df_emp2_01d = df_emp[df_emp['deptno'] == 10]
    print("dataFrame->\n",df_emp2_01d[['ename','job','sal']].sort_values(by='sal', ascending=False))
def f_2_02():
    str_2_02 = "select  empno, deptno, sal, ename, job  from emp order by deptno, sal desc"
    df_emp2_02 = pd.io.sql.read_sql(str_2_02, connection)
    print('SQL ->\n',df_emp2_02)
    print("dataFrame->\n", df_emp[['empno', 'deptno', 'sal', 'ename', 'job']].sort_values(by=['deptno', 'sal'], \
        ascending=[True, False]).reset_index(drop=True))
def f_2_03():
    print("-----------------  2.03  ---------------------------")
    str_2_03 = "SELECT ename, job FROM emp ORDER BY substr(job, length(job)-1)"
    df_emp2_03 = pd.io.sql.read_sql(str_2_03, connection)
    print('SQL ->\n',df_emp2_03)
    print("dataFrame->\n", df_emp[['ename','job']].sort_values(by='job', key=lambda x: x.str[-2:]).reset_index(drop=True))
def f_2_04():
    # str_2_04_drop = "drop view if exists V"
    # cursor.execute(str_2_04_drop)    
    str_2_04 = "create view if not exists V  as select ename || ' ' || deptno as data from emp"
    str_2_04a = "select * from V"
    # str_2_04b = "select data from V order by replace(data, replace( translate (data, \
    # '0123456789', '##########'), '#', ' '), '')"
    # str_2_04b = """SELECT data FROM V ORDER BY REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(data,
    #     '0', '#'), 
    #     '1', '#'), 
    #     '2', '#'), 
    #     '3', '#'), 
    #     '4', '#'), 
    #     '5', '#'), 
    #     '6', '#'), 
    #     '7', '#'), 
    #     '8', '#'), 
    #     '9', '#');"""
#     str_2_04b = """
#     SELECT ename || ' ' || deptno AS data 
#     FROM V 
#     ORDER BY REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(data,
#         '0', '#'), 
#         '1', '#'), 
#         '2', '#'), 
#         '3', '#'), 
#         '4', '#'), 
#         '5', '#'), 
#         '6', '#'), 
#         '7', '#'), 
#         '8', '#'), 
#         '9', '#')
# """  
    str_2_04b = """SELECT data FROM V 
ORDER BY REPLACE(data, '0', '#') || REPLACE(data, '1', '#') || REPLACE(data, '2', '#') ||
         REPLACE(data, '3', '#') || REPLACE(data, '4', '#') || REPLACE(data, '5', '#') ||
         REPLACE(data, '6', '#') || REPLACE(data, '7', '#') || REPLACE(data, '8', '#') ||
         REPLACE(data, '9', '#');"""
      
    cursor.execute(str_2_04)
    cursor.execute(str_2_04a)
    cursor.execute(str_2_04b)   #  эта строка не сортирует 
    df_emp2_04 = pd.io.sql.read_sql(str_2_04b, connection)
    print('SQL ->\n',df_emp2_04)
    df_emp2_04d = df_emp.copy()
    df_emp2_04d['data'] = df_emp['ename'] + ' ' + df_emp['deptno'].astype(str)
    df_print = df_emp2_04d[['data','deptno']].sort_values(by='deptno')
    df_print = df_emp2_04d[['data','deptno']].sort_values(by='deptno')
    print("dataFrame->\n",df_print[['data']].reset_index(drop=True))
    df_print = df_emp2_04d[['data','ename']].sort_values(by='ename')
    print("dataFrame->\n",df_print[['data']].reset_index(drop=True))
def f_2_05():
    str_2_05 = "select ename,sal,comm  from emp  order by 3 desc"
    df_emp2_05 = pd.io.sql.read_sql(str_2_05, connection)
    print('SQL ->\n',df_emp2_05)


    









