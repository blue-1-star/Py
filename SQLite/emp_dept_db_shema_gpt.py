import sqlite3

pa = 'G:\\Programming\\Py\\SQLite\\Data\\'
fi = "my_dbase.db"
pafi = pa + fi

connection = sqlite3.connect(pafi)
cursor = connection.cursor()

# Создание таблицы
create_table_sql = """
CREATE TABLE IF NOT EXISTS emp (
  empno INTEGER NOT NULL PRIMARY KEY,
  ename TEXT NOT NULL,
  job TEXT NOT NULL,
  mgr INTEGER,
  hiredate TEXT,
  sal DECIMAL(10,2),
  comm DECIMAL(10,2),
  deptno INTEGER NOT NULL
);
"""
cursor.execute(create_table_sql)

# Вставка данных
insert_data_sql = """
INSERT INTO emp VALUES 
  (7369,'SMITH','CLERK',7902,'93/6/13',800,0.00,20),
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
cursor.execute(insert_data_sql)

# cursor.execute("DROP TABLE IF EXISTS emp")
connection.commit()
connection.close()
