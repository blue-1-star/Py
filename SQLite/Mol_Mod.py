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
str_emp= "select * from emp"
str_dpt =   "select * from dept"
df_emp = pd.io.sql.read_sql(str_emp, connection) 
df_dpt = pd.io.sql.read_sql(str_dpt, connection)
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
    print("SQL->\n", df_v2)
    df_emp1 = df_emp.reset_index(drop=True)
    df_v2 = df_v2.reset_index(drop=True)
    if df_emp1.equals(df_v2, check_index=False):
        print(" Equals dataframes")
    else:
        differ = df_emp1.compare(df_v2)
        print("differeces:\n",differ)

















    









