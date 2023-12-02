import sqlite3
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------------------------
pa='G:\\Programming\\Py\\SQLite\\Data\\'
fi = "my_dbase.db"
pafi = pa + fi
connection = sqlite3.connect(pafi)
cursor = connection.cursor()

str_sql_emp_tbl = """
CREATE TABLE IF NOT EXISTS emp (
empno INTEGER NOT NULL PRIMARY KEY,
ename TEXT NOT NULL,
job TEXT NOT NULL,
mgr INTEGER,
hiredate TEXT, -- or DATE if supported
sal DECIMAL(10,2),
comm DECIMAL(10,2),
deptno INTEGER NOT NULL
);
"""
str_sql_emp_ins="""
insert into emp values (7369,'SMITH','CLERK',7902,'93/6/13',800,0.00,20),
 (7499,'ALLEN','SALESMAN',7698,'98/8/15',1600,300,30),
 (7521,'WARD','SALESMAN',7698,'96/3/26',1250,500,30),
 (7566,'JONES','MANAGER',7839,'95/10/31',2975,null,20),
 (7698,'BLAKE','MANAGER',7839,'92/6/11',2850,null,30),
 (7782,'CLARK','MANAGER',7839,'93/5/14',2450,null,10),
 (7788,'SCOTT','ANALYST',7566,'96/3/5',3000,null,20),
 (7839,'KING','PRESIDENT',null,'90/6/9',5000,0,10),
 (7844,'TURNER','SALESMAN',7698,'95/6/4',1500,0,30),
 (7876,'ADAMS','CLERK',7788,'99/6/4',1100,null,20),
 (7900,'JAMES','CLERK',7698,'00/6/23',950,null,30),
 (7934,'MILLER','CLERK',7782,'00/1/21',1300,null,10),
 (7902,'FORD','ANALYST',7566,'97/12/5',3000,null,20),
 (7654,'MARTIN','SALESMAN',7698,'98/12/5',1250,1400,30);
"""

str_sql_dept_tbl= """
CREATE TABLE IF NOT EXISTS dept(
deptno int(2) not null primary key,
dname varchar(50) not null,
location varchar(50) not null);
"""
str_sql_dept_ins="""
insert into dept values 
(10,'Accounting','New York'),
(20,'Research','Dallas'),
(30,'Sales','Chicago')
(40,'Operations','Boston');
"""
str_sql_sal_tbl="""
CREATE TABLE IF NOT EXISTS salgrade(
grade int(4) not null primary key,
losal decimal(10,2),
hisal decimal(10,2));
"""

str_sql_sal_ins="""
insert into salgrade values
(1,700,1200),
(2,1201,1400),
(3,1401,2000),
(4,2001,3000),
(5,3001,99999);
"""

# cursor.execute(str_sql_cr)
# cursor.execute(str_sql_ins)
# cursor.execute(str_sql_dept_tbl)
# cursor.execute(str_sql_dept_ins)
# cursor.execute(str_sql_sal_tbl)
# cursor.execute(str_sql_sal_ins)

# Ex 1.2

str_1_2= "select *  from emp"
str_1_3= "select *  from emp where deptno = 10 \
or comm is not null \
or sal <= 2000 and deptno=20"
# cursor.execute(str_1_2)
cursor.execute(str_1_3)
results = cursor.fetchall()
print(results)
df_emp = pd.io.sql.read_sql(str_1_2, connection, index_col='empno')
df_emp_f = pd.io.sql.read_sql(str_1_3, connection, index_col='empno')
print(df_emp)  
# print(f"-----------------",df_emp.count(), "----------------------------")
# print("\nrecords=", df_emp.count())
print(df_emp_f)  
# print("\nrecords=", df_emp_f.count())
connection.commit()
connection.close()

# -------------------------------------------------------------------------
# https://www.cems.uwe.ac.uk/~pchatter/resources/html/emp_dept_data+schema.html
"""
DROP TABLE IF EXISTS dept;
DROP TABLE IF EXISTS salgrade;
DROP TABLE IF EXISTS emp;

CREATE TABLE salgrade(
grade int(4) not null primary key,
losal decimal(10,2),
hisal decimal(10,2));

CREATE TABLE dept(
deptno int(2) not null primary key,
dname varchar(50) not null,
location varchar(50) not null);

CREATE TABLE emp(
empno int(4) not null primary key,
ename varchar(50) not null,
job varchar(50) not null,
mgr int(4),
hiredate date,
sal decimal(10,2),
comm decimal(10,2),
deptno int(2) not null);

insert into dept values (10,'Accounting','New York');

insert into dept values (20,'Research','Dallas');

insert into dept values (30,'Sales','Chicago');

insert into dept values (40,'Operations','Boston');



insert into emp values (7369,'SMITH','CLERK',7902,'93/6/13',800,0.00,20);

insert into emp values (7499,'ALLEN','SALESMAN',7698,'98/8/15',1600,300,30);

insert into emp values (7521,'WARD','SALESMAN',7698,'96/3/26',1250,500,30);

insert into emp values (7566,'JONES','MANAGER',7839,'95/10/31',2975,null,20);

insert into emp values (7698,'BLAKE','MANAGER',7839,'92/6/11',2850,null,30);

insert into emp values (7782,'CLARK','MANAGER',7839,'93/5/14',2450,null,10);

insert into emp values (7788,'SCOTT','ANALYST',7566,'96/3/5',3000,null,20);

insert into emp values (7839,'KING','PRESIDENT',null,'90/6/9',5000,0,10);

insert into emp values (7844,'TURNER','SALESMAN',7698,'95/6/4',1500,0,30);

insert into emp values (7876,'ADAMS','CLERK',7788,'99/6/4',1100,null,20);

insert into emp values (7900,'JAMES','CLERK',7698,'00/6/23',950,null,30);

insert into emp values (7934,'MILLER','CLERK',7782,'00/1/21',1300,null,10);

insert into emp values (7902,'FORD','ANALYST',7566,'97/12/5',3000,null,20);

insert into emp values (7654,'MARTIN','SALESMAN',7698,'98/12/5',1250,1400,30);


insert into salgrade values (1,700,1200);

insert into salgrade values (2,1201,1400);

insert into salgrade values (3,1401,2000);

insert into salgrade values (4,2001,3000);

insert into salgrade values (5,3001,99999);
"""
