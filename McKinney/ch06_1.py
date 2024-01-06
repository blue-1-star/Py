# Вместо !cat examples/ex1.csv
import pandas as pd
# with open('McKinney/examples/ex1.csv', 'r') as file:
    # print(file.read())
ph = "McKinney/examples/"
ph_d = "McKinney/datasets/mta_perf/"
df1 = pd.read_csv("McKinney/examples/ex1.csv", header=None)
print(df1)
df2 = pd.read_csv("McKinney/examples/ex2.csv", names=["a", "b", "c", "d", "message"])
print(df2)
names = ["a", "b", "c", "d", "message"]
df3 = pd.read_csv("McKinney/examples/ex2.csv", names=names, index_col="message")
print(df3)
parsed = pd.read_csv(ph+"csv_mindex.csv",
index_col=["key1", "key2"])
print(parsed)
result = pd.read_csv(ph+ "ex3.txt", sep="\s+")
print(result)
result = pd.read_csv(ph+ "ex4.csv", skiprows=[0,2,3])
print(f' skiprows->\n{result}')
result = pd.read_csv(ph + "ex5.csv")
print(f'ex5.csv  NaN->\n{result}')
import sys
data = pd.read_csv(ph + "ex5.csv")
data.to_csv(sys.stdout, sep="|")
data.to_csv(sys.stdout, na_rep="NULL")
# p 196
import csv
f = open(ph + "ex7.csv")
reader = csv.reader(f)
for line in reader:
    print(line)
f.close()    
with open(ph + "ex7.csv") as f:
    lines = list(csv.reader(f))
header, values = lines[0], lines[1:]
data_dict = {h: v for h, v in zip(header, zip(*values))}
print(data_dict)

# p 198
obj = """
{"name": "Wes",
"cities_lived": ["Akron", "Nashville", "New York", "San Francisco"],
"pet": null,
"siblings": [{"name": "Scott", "age": 34, "hobbies": ["guitars", "soccer"]},
{"name": "Katie", "age": 42, "hobbies": ["diving", "art"]}]
}
"""
import json
res = json.loads(obj)
print(res)
data = pd.read_json(ph + "example.json")
print(data)
data.to_json(sys.stdout)
print()
data.to_json(sys.stdout, orient="records")
tables = pd.read_html(ph +"fdic_failed_bank_list.html")
print(f'\ntables {len(tables)}')
failures = tables[0]
print(failures.head())
from lxml import objectify
with open(ph_d + "Performance_MNR.xml") as f:
    parsed = objectify.parse(f)
root = parsed.getroot()    
data =[]
skip_fields = ["PARENT_SEQ", "INDICATOR_SEQ",
"DESIRED_CHANGE", "DECIMAL_PLACES"]
for elt in root.INDICATOR:
    el_data = {}
    for child in elt.getchildren():
        if child.tag in skip_fields:
            continue
        el_data[child.tag] = child.pyval
    data.append(el_data)
perf = pd.DataFrame(data)
print(perf.head())
perf2 = pd.read_xml(ph_d + "Performance_MNR.xml")
print(perf2.head())
print(df2)
df2.to_pickle(ph + "df2_pickle")
df2_p = pd.read_pickle(ph + "df2_pickle")
print(f'From pickle ->\n{df2_p}')
xlsx = pd.ExcelFile(ph + "ex1.xlsx")
print(xlsx.sheet_names)
dfe = xlsx.parse(sheet_name="Sheet1")
print(dfe)
dfe1 = xlsx.parse(sheet_name="Sheet1", index_col=0)
print(dfe1)
dfe2 = pd.read_excel(ph + "ex1.xlsx", sheet_name="Sheet1")
print(dfe2)
# p 208
import requests
import sqlalchemy as sqla
import sqlite3
query = """
CREATE TABLE IF NOT EXISTS test
(a VARCHAR(20), b VARCHAR(20),
c REAL, d INTEGER);
"""
con = sqlite3.connect("mydata.sqlite")
con.execute(query)
con.commit()
data = [("Atlanta", "Georgia", 1.25, 6),
("Tallahassee", "Florida", 2.6, 3),
("Sacramento", "California", 1.7, 5)]
# stmt = "TRUNCATE TABLE test; INSERT INTO test VALUES(?, ?, ?, ?)"
stmt0 = "DELETE FROM test;"
stmt = "INSERT INTO test VALUES (?, ?, ?, ?);"
con.execute(stmt0)
con.executemany(stmt, data)
con.commit()
cursor = con.execute("SELECT * FROM test")
rows = cursor.fetchall()
print(rows)
# print(cursor.description)
# print(pd.DataFrame(rows, columns=[x[0] for x in cursor.description]))
import sqlalchemy as sqla
import os
# filename = "mydata.sqlite"
# full_path = os.path.join(ph, filename) 
# db_path = f"sqlite:///{full_path}"
# db = sqla.create_engine("sqlite:///examples/mydata.sqlite")
# db = sqla.create_engine(db_path)
db = sqla.create_engine("sqlite:///mydata.sqlite")   # data is created in memory
mydata = pd.read_sql("SELECT * FROM test", db)
print(f'sqlalchemy->\n{mydata}')




