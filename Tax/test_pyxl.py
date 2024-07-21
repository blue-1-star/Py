import openpyxl

# Создание новой рабочей книги
wb = openpyxl.Workbook()

# Выбор активного листа
ws = wb.active

# Запись данных в ячейки
ws['A1'] = 'Привет'
ws['B1'] = 'Мир'

# Сохранение рабочей книги в файл
# file_path = 'C:/path/to/your/directory/example.xlsx'
file_path = r'D:\Programming\Py\Tax\data\test.xlsx'
wb.save(file_path)

