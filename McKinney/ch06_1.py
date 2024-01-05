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



