import pandas as pd
import tabula
from tabula import read_pdf

# Укажите путь к вашему PDF-файлу
# file_path = "G:\Book\Biology\Дубровский\aref_Dubrovski.pdf"
# file_path = "G:\\Book\\Biology\\Дубровский\\aref_Dubrovski.pdf"
file_path = "G:\\Programming\\Py\\McKinney\\datasets\\camelot_learn\\foo.pdf"
# file_path ="chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/http://hydrobio.kiev.ua/images/Aspirantura/zahyst/aref_Dubrovski.pdf"
ph = "G:\\Programming\\Py\\McKinney\\datasets\\Dubr\\"
ph1 = "G:\\Programming\\Py\\McKinney\\datasets\\camelot_learn\\"
# Чтение данных из PDF и создание объекта DataFrame
# pages_of_interest = [6,7]
# df = read_pdf(file_path, pages='pages_of_interest')
# df = read_pdf(file_path, pages='all')
# print(f'Number of Tables=  {len(df)}')
# Вывод полученного DataFrame
# print(f'table 1\n{df[0]}\n------------------------------------\n')
# print(f'table 2\n{df[1]}\n------------------------------------\n')
# print(f'table 3\n{df[2]}\n------------------------------------\n')
# print(f'table 4\n{df[3]}\n------------------------------------\n')
# tbl_02= df[[1][4:]]

# tbl_02a= tbl_02.iloc[4:]
# print(tbl_02a)
# tabula.convert_into(file_path, ph+"output.csv", output_format="csv", pages='all')
# текст с кракозябрами и каша
import camelot
import ghostscript
# df = camelot.read_pdf(file_path)
# tables = camelot.read_pdf(file_path, flavor='stream',pages='all', process_all=True )
tables = camelot.read_pdf(file_path)
# df = camelot.read_pdf(file_path, flavor='lattice')
print(f'camelot ->\n{len(tables)}')
print(tables[0])
print(tables[0].parsing_report)
# tables.export(ph1+'foo.csv', f='csv', compress=True) 
tables.export(ph1+'foo.csv', f='csv') 
# tables.export(ph1+'foo.xlsx', f='excel') 
tables[0].to_html(ph1+'foo.html')
tables[0].to_csv(ph1+'foo1.csv')
tables[0].to_excel(ph1+'foo.xlsx', encoding='utf-8')
print(tables[0].df)
# tbl_02a.to_excel(ph+"tbl_02a.xlsx", index = False)
# tbl_01= df[0]
# tbl_02= df[1]
# tbl_03= df[2]
# tbl_04= df[3]
# tbl_05= df[4]
# tbl_06= df[5]
# with pd.ExcelWriter(ph+"tables_1.xlsx", engine='xlsxwriter') as writer:
#     tbl_01.to_excel(writer, sheet_name="Sheet1", index = False)
#     tbl_02.to_excel(writer, sheet_name="Sheet2", index = False)
#     tbl_03.to_excel(writer, sheet_name="Sheet3", index = False)
#     tbl_04.to_excel(writer, sheet_name="Sheet4", index = False)
#     tbl_05.to_excel(writer, sheet_name="Sheet5", index = False)
#     tbl_06.to_excel(writer, sheet_name="Sheet6", index = False)
# print("All Sheets created!") 
# Обработка данных из таблиц





