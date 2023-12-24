import pandas as pd
df = pd.DataFrame({
    'Courses' :['Spark','Python','Java'],
    'Fee' :[22000,25000,23000,],
    'Duration':['30days','50days','30days']
          })
print("Create DataFrame\n",df)
# Specific Value
df2=df[df['Courses'].isin(['Spark'])]
print(df2)
df2=df[df['Courses'].isin(['Spark','Java'])]
print(df2)
lst=['Spark','Python',23000,'50days',22000]
lst1=['Spark','Python',23000,'50days',22000, 111, 25000 ]
print(df.isin(['Spark','Python',23000,'50days']))
print(f'lst->\n {df.isin(lst)}')
print(f'lst1->\n {df.isin(lst1)}')




