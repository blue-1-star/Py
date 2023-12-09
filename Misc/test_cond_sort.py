import pandas as pd

# Создаем DataFrame для примера
data = {'JOB': ['SALESМAN', 'MANAGER', 'SALESМAN', 'CLERK'],
        'SAL': [5000, 6000, 4500, 3000],
        'COMM': [1000, 800, 1200, 0]}

df = pd.DataFrame(data)

# Условная сортировка
sorted_df = df.sort_values(by=['JOB', 'COMM' if 'SALESМAN' in df['JOB'].values else 'SAL'])
# print(sorted_df)


# Ваш DataFrame
df_emp = pd.DataFrame({
    'ename': ['TURNER', 'ALLEN', 'WARD', 'SMITH', 'JAMES', 'ADAMS', 'MILLER', 'MARTIN', 'CLARK', 'BLAKE', 'JONES', 'SCOTT', 'FORD', 'KING'],
    'sal': [1500, 1600, 1250, 800, 950, 1100, 1300, 1250, 2450, 2850, 2975, 3000, 3000, 5000],
    'job': ['SALESMAN', 'SALESMAN', 'SALESMAN', 'CLERK', 'CLERK', 'CLERK', 'CLERK', 'SALESMAN', 'MANAGER', 'MANAGER', 'MANAGER', 'ANALYST', 'ANALYST', 'PRESIDENT'],
    'comm': [None, 300, 500, None, None, None, None, 1400, None, None, None, None, None, None]
})

# Условие для сортировки
condition = 'salesman' in df_emp['job'].str.lower().values

# Создаем столбец для сортировки
df_emp['sort_column'] = df_emp.apply(lambda row: row['comm'] if condition else row['sal'], axis=1)

# Сортируем DataFrame
df_emp2_06d = df_emp.sort_values(by='sort_column').drop(columns=['sort_column']).reset_index(drop=True)

# Вывод результата
print(df_emp2_06d[['ename', 'sal', 'job', 'comm']])

# -------------------------------
# import pandas as pd

# Создаем DataFrame для виртуальной таблицы t1
t1_data = {'ename_and_dname': ['----------'], 'deptno': [None]}
df_t1 = pd.DataFrame(t1_data)

# Создаем DataFrame для таблицы emp (замените этот блок на ваш запрос SQL)
str_emp = "select ename as ename_and_dname, deptno from emp where deptno = 10"
df_emp = pd.io.sql.read_sql(str_emp, connection)

# Создаем DataFrame для таблицы dept (замените этот блок на ваш запрос SQL)
str_dept = "select dname, deptno from dept"
df_dept = pd.io.sql.read_sql(str_dept, connection)

# Объединяем DataFrames
result_df = pd.concat([df_emp, df_t1, df_dept], ignore_index=True)

# Выводим результат
print(result_df)
