import pandas as pd
ph = "G:\\Programming\\Py\\McKinney\\datasets\\Dubr\\"
dfe2 = pd.read_excel(ph + "tables.xlsx", sheet_name="Sheet2", skiprows=5)
dfe2e = pd.read_excel(ph + "tables.xlsx", sheet_name="Sheet7")
# print(dfe2)
print(dfe2.dtypes)
print(f'Sheet7->\n{dfe2e.dtypes}')
# dfe2 = dfe2.dropna(axis="columns", how="all")
# dfe2 = dfe2.iloc[4:]
dfe2e = dfe2.dropna(axis="columns", how="all")
for column in dfe2e.columns:
    dfe2e[column] = pd.to_numeric(dfe2e[column], errors='coerce')
for column in dfe2e.columns:
    # print(f"Before replacing in {column}:")
    # print(dfe2[column])
    if pd.api.types.is_numeric_dtype(dfe2e[column]):
        # dfe2[column] = dfe2[column].astype(str).str.replace(",", ".").astype(float)
        # dfe2[column] = dfe2[column].apply(lambda x: str(x).replace(",", ".")).astype(float)
        dfe2e[column] = dfe2e[column].astype(str).apply(lambda x: x.replace(",", ".")).astype(float)
    # print(f"After replacing in {column}:")
    # print(dfe2[column])
# print(dfe2)
print(dfe2e)
print(dfe2e.dtypes)
