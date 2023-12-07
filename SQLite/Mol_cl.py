import Mol_Mod as mm
from Mol_Mod import f_1_03, f_1_04, f_1_05, f_1_06, f_1_07, f_1_08, f_1_09
# import sqlite3
# import pandas as pd
# from pandas import Series, DataFrame
# import numpy as np
# import datetime
# from datetime import datetime, date
# import matplotlib.pyplot as plt
# pa='G:\\Programming\\Py\\SQLite\\Data\\'
# fi = "my_dbase.db"
# pafi = pa + fi
# connection = sqlite3.connect(pafi)
# cursor = connection.cursor()
# str0= "select * from emp"
# df_emp = pd.io.sql.read_sql(str0, connection) 
# def f_1_03():
#     print("-----------------  1.03---------------------------")
#     str_1_03 = "select * from emp \
#         where ( deptno = 10 \
#         or comm is not null \
#         or sal <= 2000) \
#         and deptno=20"
#     df_emp1_03 = pd.io.sql.read_sql(str_1_03, connection)
#     print(df_emp1_03)
#     df_emp1_03d = df_emp[((df_emp['deptno'] == 10) | (~df_emp['comm'].isnull()) | (df_emp['sal'] <= 2000)) & (df_emp['deptno'] == 20)]
#     first_part = (df_emp['deptno'] == 10) | (~df_emp['comm'].isnull()) | (df_emp['sal'] <= 2000)
#     sec_part = (df_emp['deptno'] == 20)
#     df_emp1_03d = df_emp[first_part & sec_part]
#     print("dataFrame___")
#     print(df_emp1_03d)                  
# def f_1_04():
#     # print('--- 1.02 ---')   
#     print("-----------------  1.04---------------------------")
#     str1_04 = 'select ename,deptno,sal from emp'
#     df_emp1_04 = pd.io.sql.read_sql(str1_04, connection)
#     print(df_emp1_04)
#     df_emp_1_04d=df_emp[['ename','deptno','sal']]
#     print(df_emp_1_04d)        
class Mol:
    
    def set(self,st):
        self.st = st
    def __init__(self,st):
        self.st = st
                # print(self.df)
        if self.st == '1.03':
            f_1_03()
        elif self.st == '1.04':
            f_1_04()
        elif self.st == '1.05':
            f_1_05()
        elif self.st == '1.06':
            f_1_06()
        elif self.st == '1.07':
            f_1_07() 
        elif self.st == '1.08':
            f_1_08()
        elif self.st == '1.09':
            f_1_09()
        else:
            print('Not in range')                   
st='1.09'
mol = Mol(st)


