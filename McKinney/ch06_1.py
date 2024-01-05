# Вместо !cat examples/ex1.csv
import pandas as pd
# with open('McKinney/examples/ex1.csv', 'r') as file:
    # print(file.read())
ph = "McKinney/examples/"
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



