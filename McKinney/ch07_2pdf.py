import pandas as pd
import tabula
from tabula import read_pdf

# Укажите путь к вашему PDF-файлу
# file_path = "G:\Book\Biology\Дубровский\aref_Dubrovski.pdf"
file_path = "G:\\Book\\Biology\\Дубровский\\aref_Dubrovski.pdf"
ph = "G:\\Programming\\Py\\McKinney\\datasets\\Dubr\\"
# Чтение данных из PDF и создание объекта DataFrame
# pages_of_interest = [6,7]
# df = read_pdf(file_path, pages='pages_of_interest')
df = read_pdf(file_path, pages='all')
print(f'Number of Tables=  {len(df)}')
# Вывод полученного DataFrame
# print(f'table 1\n{df[0]}\n------------------------------------\n')
# print(f'table 2\n{df[1]}\n------------------------------------\n')
# print(f'table 3\n{df[2]}\n------------------------------------\n')
# print(f'table 4\n{df[3]}\n------------------------------------\n')
# tbl_02= df[[1][4:]]
tbl_01= df[0]
tbl_02= df[1]
tbl_03= df[2]
tbl_04= df[3]
tbl_05= df[4]
tbl_06= df[5]

tbl_02a= tbl_02.iloc[4:]
# print(tbl_02a)
# tabula.convert_into(file_path, ph+"output.csv", output_format="csv", pages='all')
# текст с кракозябрами и каша
# tbl_02a.to_excel(ph+"tbl_02a.xlsx", index = False)
with pd.ExcelWriter(ph+"tables.xlsx", engine='xlsxwriter') as writer:
    tbl_01.to_excel(writer, sheet_name="Sheet1", index = False)
    tbl_02.to_excel(writer, sheet_name="Sheet2", index = False)
    tbl_03.to_excel(writer, sheet_name="Sheet3", index = False)
    tbl_04.to_excel(writer, sheet_name="Sheet4", index = False)
    tbl_05.to_excel(writer, sheet_name="Sheet5", index = False)
    tbl_06.to_excel(writer, sheet_name="Sheet6", index = False)
print("All Sheets created!") 


