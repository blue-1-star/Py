import sqlite3
import pandas as pd
from pandas import Series, DataFrame, concat, merge
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
pa='G:\\Programming\\Py\\SQLite\\Data\\'
fi = "my_dbase.db"
pafi = pa + fi
connection = sqlite3.connect(pafi)
cursor = connection.cursor()
# update value null in table emp.mgr for KING
# str_upd_King = "UPDATE emp SET mgr = 0 WHERE  ename = 'KING';"
# cursor.execute(str_upd_King)
str_emp= "select * from emp"
str_dpt =   "select * from dept"
str_bon =   "select * from emp_bonus"
# df_emp = pd.io.sql.read_sql(str_emp, connection, dtype={'mgr': 'Int64'}) 
df_emp = pd.io.sql.read_sql(str_emp, connection) 
# print("First appearаnce df_emp:") 
# print(df_emp.info())
# print(df_emp)
df_dpt = pd.io.sql.read_sql(str_dpt, connection)
df_bon = pd.io.sql.read_sql(str_bon, connection)
# print("emp_bonus:\n",df_bon)
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
    # str_2_05 = "select ename,sal,comm  from emp  order by 3 desc"
    str_2_05 = """select ename,sal,comm  from (select ename,sal,comm, 
                case when comm is null then 0 else 1 end as is_null 
                from emp ) x  
                order by is_null desc,comm"""
# /* ЗНАЧЕНИЯ HE-NULL СТОЛБЦА СОММ СОРТИРУЮТСЯ ПО ВОЗРАСТАНИЮ,
# ВСЕ ЗНАЧЕНИЯ NULL РАЗМЕШАЮТСЯ В КОНЦЕ СПИСКА */                
    df_emp2_05 = pd.io.sql.read_sql(str_2_05, connection)
    print('SQL ->\n',df_emp2_05)
    df_emp2_05d = df_emp[['ename','sal', 'comm']]
    def null_to_flag(value):
        if pd.isnull(value):  # Проверяем, является ли значение None или NaN
            return 0
        else:
            return 1
    # df_emp2_05d[['is_null']] = df_emp['comm'].apply(null_to_flag())
    #df_emp2_05d['is_null'] = df_emp['comm'].apply(null_to_flag)   # pandas выдыл предупреждение:
    """
    SettingWithCopyWarning:
        A value is trying to be set on a copy of a slice from a DataFrame.
        Try using .loc[row_indexer,col_indexer] = value instead
    """
    df_emp2_05d.loc[:,'is_null'] = df_emp['comm'].apply(null_to_flag)  # it still doesn't eliminate the warning
    # df_emp2_05d['is_null'] = df_emp['comm'].apply(null_to_flag)    
    df_emp2_05d = df_emp2_05d.sort_values(by=['is_null', 'comm'], \
        ascending=[False, True]) 
    print("dataFrame->\n",df_emp2_05d[['ename','sal','comm']].reset_index(drop=True))

def f_2_06():
    str_2_06 = "select ename,sal,job,comm from emp \
     order by case when job = 'SALESMAN' then comm else sal end"
    df_emp2_06 = pd.io.sql.read_sql(str_2_06, connection)
    print('SQL ->\n',df_emp2_06)
    # df_emp2_06d = df_emp.sort_values(by=['job','comm' if 'salesman' in df_emp['job'].values else 'sal'])
    #condition = 'salesman' in df_emp['job'].values
    #df_emp2_06d = df_emp.sort_values(by=np.where(condition, 'comm', 'sal'))
    # df_emp2_06d = df_emp.sort_values(by=['job','comm' if 'salesman' in df_emp['job'].values else 'sal'], na_position='last')
    # print("dataFrame->\n",df_emp2_06d[['ename','sal','job','comm']].reset_index(drop=True))
    #
    # Условие для сортировки
    condition = 'salesman' in df_emp['job'].str.lower().values

    # Создаем столбец для сортировки
    df_emp2_06d = df_emp.copy()
    df_emp2_06d['sort_column'] = df_emp.apply(lambda row: row['comm'] if condition else row['sal'], axis=1)
    # Сортируем DataFrame
    df_emp2_06d = df_emp2_06d.sort_values(by='sort_column').drop(columns=['sort_column']).reset_index(drop=True)
    print("dataFrame->\n",df_emp2_06d[['ename','sal','job','comm']].reset_index(drop=True))
def f_3_01():
    str_3_01 = """
    select ename as ename_and_dname, deptno  from emp 
    where deptno = 10 
    union all 
    select '----------' null  from t1 
    union all 
    select dname, deptno from dept
    """
    # df_emp3_01 = pd.io.sql.read_sql(str_3_01, connection)
    # print('SQL ->\n',df_emp3_01)
    
    # Создаем DataFrame для виртуальной таблицы t1
    t1_data = {'ename_and_dname': ['----------'], 'deptno': [None]}
    df_t1 = pd.DataFrame(t1_data)

    # Создаем DataFrame для таблицы emp (замените этот блок на ваш запрос SQL)
    str_3_01 = "select ename as ename_and_dname, deptno from emp where deptno = 10"
    df_emp3_01 = pd.io.sql.read_sql(str_3_01, connection)

    # Создаем DataFrame для таблицы dept (замените этот блок на ваш запрос SQL)
    str_dept = "select dname, deptno from dept"
    df_dept = pd.io.sql.read_sql(str_dept, connection)

    # Объединяем DataFrames
    result_df = pd.concat([df_emp3_01, df_t1, df_dept], ignore_index=True)

    # Выводим результат
    print(result_df)
def f_3_02():
    str_3_02 = "select e.ename, d.location  from emp e, dept d  where e.deptno = d.deptno  and e.deptno = 10"
    df_emp3_02 = pd.io.sql.read_sql(str_3_02, connection)
    print('SQL ->\n',df_emp3_02)
    str_dept =   "select deptno, location from dept"
    df_dept = pd.io.sql.read_sql(str_dept, connection)
    df_emp3_02 = pd.io.sql.read_sql(str_3_02, connection)
    df_emp3_02d = df_emp[df_emp['deptno']==10]
    # df_emp1_03d = df_emp[((df_emp['deptno'] == 10) | (~df_emp['comm'].isnull()) | (df_emp['sal'] <= 2000)) & (df_emp['deptno'] == 20)]
    result = pd.merge(df_emp3_02d, df_dept, on='deptno')
    print("dataFrame->\n",result[['ename','location']])
def f_3_03():
    # str_3_03 = "create view V as select ename,job,sal from emp where job = 'CLERK'"
    str_3_03a = "create view if not exists V1 as select ename,job,sal from emp where job = 'CLERK'"
    connection.execute(str_3_03a)
    str_3_03 = "select * from V1"
    df_emp3_03 = pd.io.sql.read_sql(str_3_03, connection)
    print('SQL ->\n',df_emp3_03)
    str_3_03b = """ select e.empno,e.ename,e.job,e.sal,e.deptno  from emp e, V1
         where e.ename = v1.ename  and e.job = v1.job  and e.sal = v1.sal """
    df_emp3_03b = pd.io.sql.read_sql(str_3_03b, connection)    
    print('SQL ->\n',df_emp3_03b)
    # res = df_emp[['empno','deptno']],(df_emp['job'] == 'CLERK')    
    # res = df_emp[df_emp['job'] == 'CLERK'][['empno', 'deptno']]
    # С использованием .loc
    # res = df_emp.loc[df_emp['job'] == 'CLERK', ['empno', 'deptno']]
    # С использованием синтаксиса квадратных скобок
    # res = df_emp[df_emp['job'] == 'CLERK'][['empno', 'deptno']]
    # print("dataFrame->\n",res[['ename']].reset_index(drop=True))
    # res = concat([df_emp3_03, res], axis=1)

    """
    смысл оператора  res = df_emp[df_emp['job'] == 'CLERK'][['empno', 'deptno']]
        в том, чтобы получить 2 столбца, отсутствующих в представлении V1  и
        затем объединить ( или слить)  столбцы V1 с res для требуемого результата.  
    """
    # result_df = pd.merge(df_emp3_03, res, on=['ename', 'job', 'sal'], how='left')
    # res = concat([df_emp3_03,res], ignore_index=True)
    res = df_emp[df_emp['job'] == 'CLERK'][['empno', 'ename','job','sal','deptno']]
    print("dataFrame->\n",res.reset_index(drop=True))
def f_3_04():
    str_3_04 = " select deptno from dept  except  select deptno from emp"
    str_3_04a ="select deptno from dept"
    str_3_04b ="select deptno from emp"
    df_emp3_04 = pd.io.sql.read_sql(str_3_04, connection)
    print('SQL ->\n',df_emp3_04)
    df_dpt_04a = pd.io.sql.read_sql(str_3_04a, connection)
    df_dpt_04b = pd.io.sql.read_sql(str_3_04b, connection)
    merged = pd.merge(df_dpt_04a, df_dpt_04b, on='deptno', how='outer', indicator=True)
    result_df = merged[merged['_merge'] == 'left_only'][['deptno']].reset_index(drop=True)
    # result_df = merged[merged['_merge'] == 'both'][['deptno']].reset_index(drop=True)
    # result_df = df_dpt_04a[~df_dpt_04a.isin(df_dpt_04b)].reset_index(drop=True)  -  не работает! 
    print("dataFrame ->\n", result_df)
def f_3_05():    
    """
    Из одной из двух таблиц с общим ключом нужно извлечь строки, в которых нет совпадающих данных в другой таблице.
    Например, нам нужно узнать, в каких отделах нет служащих. 
    """
    str_3_05 = """
    select d.*  from dept d left outer join emp e
    on (d.deptno = e.deptno)
    where e.deptno is null
    """
    df_emp3_05 = pd.io.sql.read_sql(str_3_05, connection)
    print('SQL ->\n',df_emp3_05)   
    # df_dpt_04a = pd.io.sql.read_sql(str_3_04a, connection)
    # df_dpt_04b = pd.io.sql.read_sql(str_3_04b, connection)
    # merged = pd.merge(df_dpt_04a, df_dpt_04b, on='deptno', how='outer', indicator=True)
    # result_df = merged[merged['_merge'] == 'left_only'][['deptno']].reset_index(drop=True)
    merged = merge(df_emp, df_dpt, on='deptno', how='outer', indicator=True)
    res = merged[merged['_merge']=='right_only'][['deptno','dname','location']].reset_index(drop=True)
    print("dataFrame ->\n", res)
def f_3_06():
    # 3.6. Добавление в запрос независимых объединений
    str_="select e.ename, d.location from emp e, dept d where e.deptno=d.deptno"
    df_ = pd.io.sql.read_sql(str_, connection)
    print('SQL ->\n',df_)
    str_a = "select e.ename, d.location,eb.received from emp e, dept d, emp_bonus eb where e.deptno=d.deptno and e.empno=eb.empno"
    str_a1 = """
    select e.ename, d.location, eb.received 
        from emp e join dept d
        on (e.deptno=d.deptno)
        left join emp_bonus eb
        on (e.empno=eb.empno)
        order by 2
    """
    df_a = pd.io.sql.read_sql(str_a, connection)
    df_a1 = pd.io.sql.read_sql(str_a1, connection)
    print('SQL ->\n',df_a)
    print("Independent Union:\n") 
    print('SQL ->\n',df_a1)
    merged = merge(df_emp, df_dpt, on='deptno', how='outer', indicator=True)
    # merged_df = pd.merge(df_emp, df_dpt[['deptno', 'location']], on='deptno', how='outer', indicator=True)
    # res_df = merged_df[merged_df['_merge'] == 'both'][['ename', 'location']].reset_index(drop=True)
    res = merged[merged['_merge']=='both'][['ename','location']].reset_index(drop=True)
    print("dataFrame ->\n", res)
    # print("dataFrame ->\n",df_a)
    # Сначала соединяем emp и dept
    merged_df = pd.merge(df_emp, df_dpt[['deptno', 'location']], on='deptno')
    # Затем левое соединение с emp_bonus
    merged_df = pd.merge(merged_df, df_emp_bonus, on='empno', how='left')
    # Выбираем нужные столбцы и сортируем результат
    result_df = merged_df[['ename', 'location', 'received']].sort_values(by='location').reset_index(drop=True)

"""
Фактически, при использовании метода pd.merge, слева стоит первый датафрейм, а справа — второй.
Таким образом, при указании how='left' мы выполняем левое соединение, то есть сохраняются все строки
 из первого (левого) датафрейма (df_emp и df_dpt), а соответствующие строки из второго (правого) датафрейма (df_emp_bonus) добавляются,
 если есть соответствие.
В вашем конкретном случае, после первого соединения (df_emp и df_dpt), мы сохраняем все строки из него и добавляем соответствующие
 строки из df_emp_bonus. Это может быть понято как "левое соединение", потому что мы берем все из "левого" датафрейма и добавляем
 соответствующие из "правого".
User
да, задача решена, но как для меня слова в SQL :
 left join emp_bonus eb  -  немного сбивают с толку - речь идет о третьем датафрейме emp_bonus  который как бы добавляется справа
 - но называем мы это левым ( ха-ха!) 
ChatGPT
Да, в терминологии SQL левое соединение (left join) подразумевает сохранение всех записей из левой (первой) таблицы и добавление
соответствующих записей из правой (второй) таблицы. Это относится к порядку указания таблиц в запросе SQL. 
Таким образом, когда вы пишете FROM emp LEFT JOIN emp_bonus, emp считается "левой" таблицей.
В pandas, метод merge использует схожую концепцию, где первый переданный датафрейм считается "левым", а второй - "правым".
Поэтому, когда мы пишем pd.merge(df_emp, df_emp_bonus, on='empno', how='left'), df_emp считается "левым" датафреймом,
и все записи из df_emp сохраняются, а соответствующие записи из df_emp_bonus добавляются, если они есть.
Это может быть немного запутывающим, когда вы сначала сталкиваетесь с этими терминами, но главное помнить,
что важно сохранить все записи из "левой" таблицы, а "правая" таблица просто добавляет соответствующие записи.
"""
def f_3_07():
    # 3.7. Проверка двух таблиц на идентичность
    str_= """create view if not exists  V2
    as
    select * from emp where deptno != 10
    union all
    select * from emp where ename = 'WARD'
"""
    cursor.execute(str_)
    str_1 = "select * from V2"
    df_v2 = pd.io.sql.read_sql(str_1, connection)
    # print("SQL->\n", df_v2)
    df_emp1 = df_emp.copy()
    # df_emp1 = df_emp.reset_index(drop=True)
    # df_v2 = df_v2.reset_index(drop=True)
    # df_emp3_02d = df_emp[df_emp['deptno']==10]
    df_v2a = df_emp1.copy()
    # df_v2a = df_emp1[df_emp1['deptno']!=10]
    df_v2a.loc['15'] = ['8888','FIRST','ROBOT','8887','99/7/20','11111','0','10']
    # print(df_v2a)
    # ss.loc['FOO'] = ['the sector', 100, 110]
    # print(df_v2a)
    # print(df_emp1.columns)
    # print(df_v2.columns)
    # print("Original emp:")
    # print(df_emp.info())
    # print("Copy emp:")
    # print(df_emp1.info())
    # print("From view V2:")
    # print(df_v2.info())
    print(df_emp1.info())     
    print(df_v2a.info()) 
    df_emp1 = df_emp1.reset_index(drop=True)
    df_v2a = df_v2a.reset_index(drop=True)      
    print(df_v2a)
    if df_emp1.equals(df_v2a):
        print(" Equals dataframes")
    else:
        differ = df_emp1.compare(df_v2a)
        print("differeces:\n",differ)
def f_3_08():
    # 3.8. Выявление и устранение проблемы декартовых произведений 
    str_ =""" select e.ename, d.location
    from emp e, dept d
    where e.deptno = 10"""
    df_ = pd.io.sql.read_sql(str_, connection)
    print(df_)    
    merged = merge(df_emp, df_dpt, on='deptno', how='outer', indicator=True)
    merged= merged[merged['deptno']==10].reset_index(drop=True)
    # merged_filtered = merged.query('deptno == 10')
    print(merged[['ename','location']])
    # merged = merge(df_emp[df_emp['deptno'] == 10], df_dpt, on='deptno', how='outer', indicator=True)
    # print(merged[['ename', 'location']])
def f_3_09():
    """ 
    вычислить суммы зарплат и премий всех служащих отдела 1О. Но некоторые служащие получили несколько премий,
    и объединение таблицы ЕМР с таблицей ЕМР_BONUS, содержащей данные о премиях сотрудников для этой задачи,
    вызывает возвращение неправильных значений агрегатной функцией suм. 
    """ 
    str_="""
    select e.empno,
    e.ename,
    e.sal,
    e.deptno,
    e.sal*case when eb.type = 1 then .1
    when eb.type = 2 then .2
    else .3
    end as bonus
    from emp e, emp_bonus eb
    where e.empno = eb.empno
    and e.deptno = 10
    """
    df_ = pd.io.sql.read_sql(str_, connection)
    print(df_)    
    str_1 = """
    select deptno,
        sum(sal) as total_sal,
        sum(bonus) as total_bonus
    from (
    select e.empno, e.ename, e.sal, e.deptno, e.sal*case when eb.type = 1 then .1
                                                        when eb. type = 2 then .2
                                                        else .3 end as bonus
    from emp e, emp_bonus eb
    where e.empno = eb.empno and e.deptno = 10) x
    group by deptno
"""
    df_1 = pd.io.sql.read_sql(str_1, connection)
    print(df_1)    
    str_2 = "select sum(sal) from emp where deptno=10"
    df_2 = pd.io.sql.read_sql(str_2, connection)
    print("df_2=\n",df_2)    
    str_3 = """select e.ename, e.sal
        from emp e, emp_bonus eb 
        where e.empno = eb.empno and e.deptno = 10"""
    df_3 = pd.io.sql.read_sql(str_3, connection)
    print("df_3=\n",df_3)    
    str_1a = """
    select deptno,
        sum(distinct sal) as total_sal,
        sum(bonus) as total_bonus
    from (
    select e.empno, e.ename, e.sal, e.deptno, e.sal*case when eb.type = 1 then .1
                                                        when eb. type = 2 then .2
                                                        else .3 end as bonus
    from emp e, emp_bonus eb
    where e.empno = eb.empno and e.deptno = 10) x
    group by deptno
    """   
    df_1a = pd.io.sql.read_sql(str_1a, connection)
    print("distinct \n",df_1a)        
    merged = merge(df_emp, df_dpt, on='deptno', how='outer', indicator=True)
    # dataframes
    merg_df = pd.merge(df_emp, df_bon, on='empno', how='inner')
    # print("df_emp merge with df_bon:")
    merg_df = merg_df[merg_df['deptno']==10]
    merg_df['bonus'] = merg_df['sal']*merg_df['type'].map({1:0.1, 2: 0.2, 3:0.3})
    # print(merg_df['bonus'])    
    print("DataFrame:")
    print(merg_df)
    res = merg_df.groupby('deptno').agg({'sal':'sum','bonus':'sum'}).reset_index()
    # res = merg_df.groupby('deptno').agg({'sal': 'sum', 'sal': 'nunique', 'bonus': 'sum'}).reset_index()
    # res = merg_df.groupby('deptno').agg({'sal': 'sum', 'sal': lambda x: x.unique().sum(), 'bonus': 'sum'}).reset_index()   
    res = merg_df.groupby('deptno').agg({'sal': lambda x: x.unique().sum(), 'bonus': 'sum'}).reset_index()   
    res.columns=['deptno','total_sal','total_bonus']
    print(res)
    """ 
    требуется ещё одно уточнение:  уникальность должна быть не по столбцу 'sal'
    а по другому - скажем 'empno' но сумма должна вычисляться по столбцу 'sal'  
    ( сумма элементов 'sal с  уникальными 'empno' . 
    
    Понял, вы хотите суммировать значения столбца 'sal', уникальные для каждого 'empno'.
    В таком случае, вам нужно использовать группировку по 'empno' и затем суммировать 'sal' для каждой группы. Пример кода:

    res = merg_df.groupby('deptno').agg({'sal': lambda x: x.groupby('empno').unique().sum(), 'bonus': 'sum'}).reset_index()
    res.columns = ['deptno', 'total_sal', 'total_bonus']

    Этот код использует groupby('empno') для создания групп для каждого уникального 'empno', 
    а затем применяет unique() и sum() для суммирования уникальных значений 'sal' в каждой группе.

    """
    str_ins = "insert into emp values (7935,'NORTON','CLERK',7902,'93/6/13',2450,null,10)"
    str_del = "DELETE FROM emp WHERE empno = '7935'"
    str_upd = "UPDATE emp SET sal = 247  WHERE empno = 7935"
    # cursor.execute(str_ins)
    # cursor.execute(str_upd)
    # connection.commit()
    df_1a = pd.io.sql.read_sql(str_1a, connection) # table emp was change but df_1a - not
    print(df_1a)        
    # cursor.execute(str_del)
    # connection.commit()
    # df_1a = pd.io.sql.read_sql(str_1a, connection)
    # print(df_1a)        
def f_3_10():
    # Постановка задачи та же, что и для рецепта 3.9, с тем отличием, что не все служащие отдела 1О получили премии,
    #  что отражено должным образом в таблице ЕМР BONUS:
    str_1 = """
    select deptno,
        sum(sal) as total_sal,
        sum(bonus) as total_bonus
    from (
    select e.empno, e.ename, e.sal, e.deptno, e.sal*case when eb.type = 1 then .1
                                                        when eb. type = 2 then .2
                                                        else .3 end as bonus
    from emp e, emp_bonus eb
    where e.empno = eb.empno and e.deptno = 10) 
    group by deptno
    """   
    df_1 = pd.io.sql.read_sql(str_1, connection)
    print(df_1)  
    str_="""
    select e.empno,
    e.ename,
    e.sal,
    e.deptno,
    e.sal*case when eb.type = 1 then .1
    when eb.type = 2 then .2
    else .3
    end as bonus
    from emp e, emp_bonus eb
    where e.empno = eb.empno
    and e.deptno = 10
    """
    df_ = pd.io.sql.read_sql(str_, connection)
    print("without -group by deptno\n",df_)    
    # выполняется внешнее объединение с таблицей ЕМР BONUS, чтобы обеспечить включение всех служащих отдела 10.
    # Answer GPT about inner and outer 
    """
    Выбор между внутренним и внешним соединением зависит от вашей задачи и того, какие данные вы хотите получить.
    Вот основные различия между ними: 
    Внутреннее соединение (how='inner'):
    Возвращает только те строки, которые имеют соответствующие значения в обеих таблицах по ключу (условию объединения).
    Используется, когда вас интересуют только те строки, которые имеют соответствие в обеих таблицах.
    Внешнее соединение (how='outer'):
    Возвращает все строки из обеих таблиц, дополняя отсутствующие значения в одной из таблиц нулями или NaN.
    Используется, когда вам нужны все строки из обеих таблиц, независимо от того, есть ли соответствие или нет.
    """
    str_1a = """
    select deptno,
        sum(distinct sal) as total_sal,
        sum(bonus) as total_bonus
    from (
    select e.empno, e.ename, e.sal, e.deptno, e.sal*case when eb.type is null then 0 
                                                        when eb.type = 1 then .1
                                                        when eb. type = 2 then .2
                                                        else .3 end as bonus
    from emp e left outer join emp_bonus eb
    on (e.empno = eb.empno)
    where  e.deptno = 10) 
    group by deptno
    """   
    df_1a = pd.io.sql.read_sql(str_1a, connection)
    print(f"with distinct in sum and left outer join emp_bonus eb\n {df_1a}") 
    # error - 2 records in emp_bonus sum = 390 but here total_bonus = 2625 ? 
    # !!  was missing a condition !!when eb.type is null then 0 !!
    # At first glance, though emp_bonus and does not contain the values of null
    # but it is not about the original emp_bonus but the  left outer join 
    # print(f'check only emp_bonus->\n {pd.io.sql.read_sql("select * from emp_bonus", connection)}')
    # Dataframes   - df_emp, df_bon  Defined in the header 
    merg_df = pd.merge(df_emp, df_bon, on='empno', how='inner')  
    merg_df = merg_df[merg_df['deptno']==10]
    merg_df['bonus'] = merg_df['sal']*merg_df['type'].map({1:0.1, 2: 0.2, 3:0.3})
    res = merg_df.groupby('deptno').agg({'sal':'sum','bonus':'sum'}).reset_index()
    print("dataframe:\n",res)
    # Выполнение left outer join
    merged_df = pd.merge(df_emp[df_emp['deptno'] == 10], df_bon, how='left', on='empno')
    print(f'all records lefr outer join:\n{merged_df}')
    merged_df['bonus'] = merged_df['sal'] * merged_df['type'].map({1: 0.1, 2: 0.2, 3: 0.3})
    merged_df_unique = merged_df.drop_duplicates(subset=['empno'])
    result_df = merged_df.groupby('deptno').agg({'sal': 'sum', 'bonus': 'sum'}).reset_index()
    result_df = merged_df.groupby('deptno').agg({'sal': lambda x: x.unique().sum(), 'bonus': 'sum'}).reset_index()
    # result_df = merged_df.groupby('deptno').agg({'sal': 'sum', 'bonus': 'sum','empno':'nunique'}).reset_index()
    # result_df.columns = ['deptno', 'total_sal', 'total_bonus', 'unique_empno']
    result_df.columns = ['deptno', 'total_sal', 'total_bonus']
    print("left outer join:\n",result_df)
def f_3_11():      # p 102
    str_left = """select d.deptno,d.dname,e.ename
    from dept d left outer join emp e
    on (d.deptno=e.deptno)"""
    df_left = pd.io.sql.read_sql(str_left, connection)
    res = pd.merge(df_dpt, df_emp, how='left', on='deptno')
    print(df_left)
    print(f"dataframe \n {res[['deptno','dname','ename','empno']].sort_values(by='empno')}")
    str_ins_emp = """insert into emp (empno,ename,job,mgr,hiredate,sal,comm,deptno)
        select 1111, 'YODA', 'JEDI', null, hiredate, sal, comm, null
        from emp
        where ename = 'KING'"""
    # cursor.execute(str_ins_emp)
    # connection.commit()
    str_right = """select d.deptno,d.dname,e.ename
    from dept d right outer join emp e
    on (d.deptno=e.deptno)"""
    df_right = pd.io.sql.read_sql(str_right, connection)
    print(df_right)
    # str_f = """ select d.deptno,d.dname,e.ename
            # from dept d full outer join emp e
            # on (d.deptno=e.deptno)"""
    str_f_gpt = """
    SELECT d.deptno, d.dname, e.ename
    FROM dept d
    LEFT JOIN emp e ON d.deptno = e.deptno

    UNION

    SELECT d.deptno, d.dname, e.ename
    FROM emp e
    LEFT JOIN dept d ON d.deptno = e.deptno
    WHERE d.deptno IS NULL;
    """
    str_f = """
    select d.deptno,d.dname,e.ename
        from dept d right outer join emp e
        on (d.deptno=e.deptno)
        union
        select d.deptno,d.dname,e.ename
        from dept d left outer join emp e
        on (d.deptno=e.deptno) """
    df_full = pd.io.sql.read_sql(str_f, connection)
    # df_full = pd.io.sql.read_sql(str_f_gpt, connection)
    print(df_full)
    df_right = pd.merge(df_emp, df_dpt, how="right", on = 'deptno' )
    df_left = pd.merge(df_emp, df_dpt, how="left", on = 'deptno')
    # df_union = pd.concat([df_right, df_left], ignore_index=True)
    df_union = pd.concat([df_right, df_left]).drop_duplicates().reset_index(drop=True)
    df_union[['empno', 'deptno']] = df_union[['empno', 'deptno']].astype('Int64') 
    print(f'DataFrame->\n {df_union}')
def f_3_12():
    str_="""
     select ename,comm
     from emp
     where coalesce(comm,0) < ( select comm from emp where ename='WARD')
    """
    df_ = pd.io.sql.read_sql(str_, connection)
    print(df_)
def f_4_05():
    str_ = """
        CREATE TABLE  IF NOT EXISTS  dept_east AS
        SELECT * FROM dept WHERE 1 = 0;
    """
    str_1 = """
        CREATE TABLE  IF NOT EXISTS  dept_mid AS
        SELECT * FROM dept WHERE 1 = 0;
    """
    
    # cursor.execute(str_)
    cursor.execute(str_1)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall() # create list of tuples with names tables
    # create from list of tuples list of items of each tuples
    # result_list = [item[0] for item in tables]
    """
    there was only one element in the tuple. If we needed all of them (i.e. there was more than one) then 
    result_list = [element for tup in list_of_tuples for element in tup]
    """
    print([item[0] for item in tables])   # 
    # 
    # for table in tables:
        # print(table[0])
def f_4_06():
# 4.6. Вставка строк одновременно в несколько таблиц p 113    
    str_1 = """
    INSERT INTO dept_east (deptno, dname, location)
SELECT deptno, dname, location
FROM dept
WHERE location IN ('New York', 'Boston');"""

    str_2 = """
INSERT INTO dept_mid (deptno, dname, location)
SELECT deptno, dname, location
FROM dept
WHERE location = 'Chicago';"""
    # cursor.execute(str_1)
    # cursor.execute(str_2)
    # connection.commit()
# Создаем целевые датафреймы
    df_dept_east = pd.DataFrame(columns=['deptno', 'dname', 'location'])
    df_dept_mid = pd.DataFrame(columns=['deptno', 'dname', 'location'])
    print(f'df_dept_east ->\n{df_dept_east.info()}')
    print(f'df_dept_mid ->\n{df_dept_mid.info()}')
    # in table dept.location  the words are in capital letters 
    # convert them through  capitalize 
    # c_str = " ".join(word.capitalize() for word in df_dpt['location'].split())
    # Условия для вставки в различные датафреймы
    condition_east = df_dpt['location'].isin(['New York', 'Boston'])
    condition_mid = df_dpt['location'] == 'Chicago'
    # Вставляем данные в соответствующие датафреймы
    #  !!!!   - однако у меня совершенно непредсказуемо вылетатет эта ошибка и найти причину не удается
    #  AttributeError: 'DataFrame' object has no attribute 'append'. Did you mean: '_append'?
    """
     Нет необходимости использовать _append, это была неправильная интерпретация ошибки.
     На самом деле, метод должен быть append, а не _append. Если у вас была такая ошибка, скорее всего, 
     это связано с другими аспектами кода или среды выполнения.
    """
    df_dept_east = df_dept_east._append(df_dpt[condition_east], ignore_index=True)
    df_dept_mid = df_dept_mid._append(df_dpt[condition_mid], ignore_index=True)
    print(f'dept_east->\n {df_dept_east} \n dept_mid\n {df_dept_mid}')
def f_4_07():
    print(f'under construction')
# ---------------------------       f_4_08    
def f_4_08():
    str_= """
    select deptno,ename,sal from emp
    where deptno = 20
    order by 1,3
    """
    
    df_ = pd.io.sql.read_sql(str_, connection)
    print(df_)
    str_f = """
    update emp  set sal = sal*1.10 where deptno = 20
    """
    cursor.execute(str_f)   # increase salary and modify database
    connection.commit()
    df_f = pd.io.sql.read_sql(str_, connection)   # show result
    print(f'change sal->\n {df_f}')
    df_emp['deptno'] = df_emp['deptno'].astype('Int64')
    condition_sal = df_emp['deptno'] == 20
    df_emp.loc[condition_sal, 'sal'] *= 1.1
    df_emp['sal'] = df_emp['sal'].astype(float)
    # df_emp.loc[condition_sal, 'sal'] = df_emp.loc[condition_sal, 'sal'] * 1.1  # Увеличение зарплаты 10%
    # df_emp.loc[condition_sal, 'sal'] = df_emp.loc[condition_sal, 'sal'].astype(float) * 1.1
    print(f"Dataframe ->\n {df_emp[['deptno', 'ename', 'sal', ]].reset_index(drop=True)}")
    df_emp_increased_salary = df_emp[condition_sal][['deptno', 'ename', 'sal']].sort_values(by=['deptno', 'sal']).reset_index(drop=True)
    print(f'DF - increased salary->\n {df_emp_increased_salary}')
    # revert the data state back 
    str_b = """
    update emp  set sal = sal/1.10 where deptno = 20
    """
    cursor.execute(str_b)    # resetting the database
    connection.commit()
    df_b = pd.io.sql.read_sql(str_, connection)
    print(f'initial state->\n{df_b}')
    str_v = """
    select deptno , ename, sal as orig_sal, 
        sal*.10 as amt_to_add,
        sal*1.10 as new_sal
        from emp
        where deptno=20
        order by 1,5
    """
    # df_v = pd.io.sql.read_sql(str_v, connection)
    # print(f'preview->\n {df_v}')

def f_4_09():
    # .9. Обновление при условии наличия соответствующих строк
    str_f = """
    update emp set sal=sal*1.20 where empno in ( select empno from emp_bonus) 
    """ 
    cursor.execute(str_f)   # increase salary and modify database
    str_r = "select empno, ename, sal  from emp where empno in ( select empno from emp_bonus)"
    df_r = pd.io.sql.read_sql(str_r, connection)
    print(f'update salary->\n {df_r} ')    
    print(f'emp_bonus->\n{df_bon}')
    mrg = pd.merge(df_emp, df_bon, on = 'empno', how = 'inner')
    print(f"merg bon and emp\n{mrg[['empno','ename']]}")
    #condition_sal =     #condition_sal = df_emp['deptno'] == 20
    df_emp.loc[condition_sal,'sal'] *= 1.2
    connection.commit()
    str_b = """
    update emp set sal=sal/1.20 where empno in ( select empno from emp_bonus) 
    """ 
    # df_emp.loc[condition_sal, 'sal'] *= 1.1
    cursor.execute(str_b)   # reset database to initial state
    connection.commit()



















    