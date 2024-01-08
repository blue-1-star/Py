import pandas as pd
ph = "G:\\Programming\\Py\\McKinney\\datasets\\Dubr\\"
dfe2 = pd.read_excel(ph + "tables.xlsx", sheet_name="Sheet2")
for column in dfe2.columns:
    if pd.api.types.is_numeric_dtype(dfe2[column]):
        # dfe2[column] = dfe2[column].astype(str).str.replace(",", ".").astype(float)
        dfe2[column] = dfe2[column].apply(lambda x: str(x).replace(",", ".")).astype(float)

def change_decimal_delim(df):  # change decimal delimiter for , to .
    df_copy = df.copy()
    # Цикл по всем столбцам
    for column in df_copy.columns:
        # Проверка, что тип данных столбца - числовой
        if pd.api.types.is_numeric_dtype(df_copy[column]):
        # Замена десятичного разделителя в текущем столбце
            df_copy[column] = df_copy[column].astype(str).str.replace(",", ".").astype(float)
            # df_copy[column] = df_copy[column].apply(lambda x: str(x).replace(",", ".")).astype(float)
    return df_copy        
# dfe2 = change_decimal_delim(dfe2)
print(dfe2)
