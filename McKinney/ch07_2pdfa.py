import camelot
import ghostscript
tables = camelot.read_pdf(file_path)
print(f'camelot ->\n{len(tables)}')
print(tables[0])
print(tables[0].parsing_report)
tables.export(ph1+'foo.csv', f='csv') 
tables[0].to_html(ph1+'foo.html')
tables[0].to_excel(ph1+'foo.xlsx',  encoding='utf-8')

