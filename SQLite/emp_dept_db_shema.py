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
insert into emp values (7369,'SMITH','CLERK',7902,'93/6/13',800,null,20),
 (7499,'ALLEN','SALESMAN',7698,'98/8/15',1600,300,30),
 (7521,'WARD','SALESMAN',7698,'96/3/26',1250,500,30),
 (7566,'JONES','MANAGER',7839,'95/10/31',2975,null,20),
 (7698,'BLAKE','MANAGER',7839,'92/6/11',2850,null,30),
 (7782,'CLARK','MANAGER',7839,'93/5/14',2450,null,10),
 (7788,'SCOTT','ANALYST',7566,'96/3/5',3000,null,20),
 (7839,'KING','PRESIDENT',0,'90/6/9',5000,null,10),
 (7844,'TURNER','SALESMAN',7698,'95/6/4',1500,null,30),
 (7876,'ADAMS','CLERK',7788,'99/6/4',1100,null,20),
 (7900,'JAMES','CLERK',7698,'00/6/23',950,null,30),
 (7934,'MILLER','CLERK',7782,'00/1/21',1300,null,10),
 (7902,'FORD','ANALYST',7566,'97/12/5',3000,null,20),
 (7654,'MARTIN','SALESMAN',7698,'98/12/5',1250,1400,30);
"""
# correct - all values comm except positive numeric   is null
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
str_sql_emp_bonus_tbl="""
CREATE TABLE IF NOT EXISTS emp_bonus(
empno int(4) not null primary key,
bonus decimal(10,2),
received TEXT,
type integer 
);  
"""
# modified structure for the table emp_bonus     
str_sql_emp_bon_tbl="""
CREATE TABLE IF NOT EXISTS emp_bonus(
id_b integer primary key autoincrement,   
empno integer,
bonus decimal(10,2),
received TEXT,
type integer 
);  
"""



str_sql_emp_bon_ins="""
insert into emp_bonus(empno, bonus, received, type) values
(7369,1200,'2005/3/14',1),
(7788,2400,'2005/3/14',2),
(7900,1890,'2005/3/14',3),
(7934,2400,'2005/3/17',1),
(7934,2400,'2005/2/15',2),
(7839,2400,'2005/2/15',3),
(7782,2400,'2005/2/15',1);
"""

# cursor.execute(str_sql_emp_tbl)
# cursor.execute(str_sql_emp_ins)
# cursor.execute(str_sql_dept_tbl)
# cursor.execute(str_sql_dept_ins)
# cursor.execute(str_sql_sal_tbl)
# cursor.execute(str_sql_sal_ins)
# cursor.execute(str_sql_emp_bonus_tbl)
# cursor.execute(str_sql_emp_bonus_ins)
# cursor.execute(str_sql_emp_bon_tbl)
# cursor.execute(str_sql_emp_bon_ins)
# Ex 1.2

str_1_2= "select *  from emp"
str_1_3= "select *  from emp where deptno = 10 \
or comm is not null \
or sal <= 2000 and deptno=20"
str_eb =  "select *  from emp_bonus"
cursor.execute(str_1_2)

cursor.execute(str_1_3)
results = cursor.fetchall()
# print(results)
# df_emp = pd.io.sql.read_sql(str_1_2, connection, index_col='empno')

df_emp = pd.io.sql.read_sql(str_1_2, connection, dtype={'mgr': 'Int64'})
df_emp_f = pd.io.sql.read_sql(str_1_3, connection, index_col='empno')
# print(df_emp)  
# print(df_emp.info())


# print(f"-----------------",df_emp.count(), "----------------------------")
# print("\nrecords=", df_emp.count())
cursor.execute(str_eb)
df_empb = pd.io.sql.read_sql(str_eb, connection,index_col='empno') #, index_col='empno')
print(df_empb)  
# print("\nrecords=", df_emp_f.count())
str_copy = "CREATE TABLE emp_bonus_c AS SELECT * FROM  emp_bonus"
cursor.execute(str_copy)
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
