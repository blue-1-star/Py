import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def add_color_columns_to_excel(input_file, output_file, columns_with_hex):
    # Читаем Excel файл в DataFrame
    df = pd.read_excel(input_file)
    
    # Загружаем файл для работы с openpyxl
    wb = load_workbook(input_file)
    ws = wb.active

    # Добавляем рядом с каждым указанным столбцом новый столбец для цвета
    for col in columns_with_hex:
        if col not in df.columns:
            print(f"Столбец '{col}' не найден в таблице. Пропуск.")
            continue

        # Создаем новый столбец рядом с исходным
        col_index = df.columns.get_loc(col) + 1  # Индекс столбца в pandas (нумерация с 0)
        new_col_name = f"{col}_Color"
        df.insert(col_index, new_col_name, "")  # Добавляем пустой столбец
        
        # Применяем цвета к ячейкам нового столбца
        for i, hex_code in enumerate(df[col]):
            if isinstance(hex_code, str) and hex_code.startswith('#') and len(hex_code) == 7:
                try:
                    # Закрашиваем ячейку
                    cell = ws.cell(row=i+2, column=col_index+1)  # i+2: сдвиг для строки заголовков
                    cell.fill = PatternFill(start_color=hex_code[1:], end_color=hex_code[1:], fill_type="solid")
                except Exception as e:
                    print(f"Ошибка обработки цвета '{hex_code}' в строке {i+2}: {e}")
            else:
                print(f"Некорректный HEX-код '{hex_code}' в строке {i+2}. Пропуск.")
    
    # Сохраняем изменения в новый файл
    wb.save(output_file)
    print(f"Файл с добавленными цветами сохранен как '{output_file}'.")

# Пример использования
add_color_columns_to_excel(
    input_file="input.xlsx",
    output_file="output_with_colors.xlsx",
    columns_with_hex=["ColorHex"]
)
