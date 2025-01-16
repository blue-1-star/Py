import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from datetime import datetime, timedelta
import os
from brightness_analysys_0a import auto_adjust_column_width 
from coloring_columns_hex_2 import insert_empty_columns 

def add_color_columns_to_excel(input_file, output_file, columns_with_hex):
    # Читаем Excel файл в DataFrame
    df = pd.read_excel(input_file)
    
    # Загружаем файл для работы с openpyxl
    wb = load_workbook(input_file)
    ws = wb.active

    # Проходим по указанным столбцам с HEX-кодами
    for col in columns_with_hex:
        if col not in df.columns:
            print(f"Столбец '{col}' не найден в таблице. Пропуск.")
            continue

        # Определяем индекс текущего столбца
        col_index = df.columns.get_loc(col) + 1  # Индекс столбца в openpyxl (нумерация с 1)
        new_col_index = col_index + 1  # Новый столбец будет добавлен сразу после текущего

        # Вставляем новый столбец в Excel
        ws.insert_cols(new_col_index)

        # Копируем данные из исходного столбца в новый
        for row in range(2, ws.max_row + 1):  # Пропускаем заголовок
            ws.cell(row=row, column=new_col_index).value = ws.cell(row=row, column=col_index).value

        # Закрашиваем ячейки нового столбца
        for i, hex_code in enumerate(df[col]):
            excel_row = i + 2  # Нумерация строк в Excel (с учётом заголовков)
            if isinstance(hex_code, str) and hex_code.startswith('#') and len(hex_code) == 7:
                try:
                    cell = ws.cell(row=excel_row, column=new_col_index)
                    cell.fill = PatternFill(start_color=hex_code[1:], end_color=hex_code[1:], fill_type="solid")
                except Exception as e:
                    print(f"Ошибка обработки цвета '{hex_code}' в строке {excel_row}: {e}")
            else:
                print(f"Некорректный HEX-код '{hex_code}' в строке {excel_row}. Пропуск.")
        
        # Добавляем название нового столбца
        ws.cell(row=1, column=new_col_index).value = f"{col}_Color"
    
    # Сохраняем изменения в новый файл
    wb.save(output_file)
    print(f"Файл с добавленными цветами сохранен как '{output_file}'.")


def fill_color_columns_to_excel1(input_file, output_file, columns_with_hex):
    # Читаем Excel файл в DataFrame
    df = pd.read_excel(input_file)
    
    # Загружаем файл для работы с openpyxl
    wb = load_workbook(input_file)
    ws = wb.active

    # Проходим по указанным столбцам с HEX-кодами
    for col in columns_with_hex:
        if col not in df.columns:
            print(f"Столбец '{col}' не найден в таблице. Пропуск.")
            continue

        # Определяем индекс текущего столбца
        col_index = df.columns.get_loc(col) + 1  # Индекс столбца в openpyxl (нумерация с 1)
        new_col_index = col_index + 1  #  столбец  для закрашивания
        # Вставляем новый столбец в Excel
        # ws.insert_cols(new_col_index)

        # Копируем данные из исходного столбца в новый
        # for row in range(2, ws.max_row + 1):  # Пропускаем заголовок
        #     ws.cell(row=row, column=new_col_index).value = ws.cell(row=row, column=col_index).value

        # Закрашиваем ячейки нового столбца
        for i, hex_code in enumerate(df[col]):
            excel_row = i + 2  # Нумерация строк в Excel (с учётом заголовков)
            if isinstance(hex_code, str) and hex_code.startswith('#') and len(hex_code) == 7:
                try:
                    cell = ws.cell(row=excel_row, column=new_col_index)
                    cell.fill = PatternFill(start_color=hex_code[1:], end_color=hex_code[1:], fill_type="solid")
                except Exception as e:
                    print(f"Ошибка обработки цвета '{hex_code}' в строке {excel_row}: {e}")
            else:
                print(f"Некорректный HEX-код '{hex_code}' в строке {excel_row}. Пропуск.")
        
        # Добавляем название нового столбца
        # ws.cell(row=1, column=new_col_index).value = f"{col}_Color"
    
    # Сохраняем изменения в новый файл
    wb.save(output_file)
    print(f"Файл с добавленными цветами сохранен как '{output_file}'.")

def fill_color_columns_to_excel(output_file, df, columns_with_hex):
    """
    Заполняет цветами ячейки в Excel на основе HEX-кодов, содержащихся в указанных столбцах.

    :param output_file: str, путь к выходному Excel-файлу
    :param df: pd.DataFrame, датафрейм с данными
    :param columns_with_hex: list, список столбцов с HEX-кодами цветов
    """
    # Сохраняем DataFrame в Excel
    df.to_excel(output_file, index=False, engine='openpyxl')

    # Открываем Excel-файл для модификации
    wb = load_workbook(output_file)
    ws = wb.active

    for col in columns_with_hex:
        if col in df.columns:
            col_index = df.columns.get_loc(col) + 1  # Индекс столбца с HEX-кодами (1-based для Excel)
            empty_col_index = col_index + 1  # Индекс пустого столбца для раскрашивания

            for row_index, hex_code in enumerate(df[col], start=2):  # Начинаем с 2, т.к. 1 строка - заголовки
                if pd.notna(hex_code):
                    try:
                        # Устанавливаем цвет ячейки в пустом столбце
                        fill = PatternFill(start_color=hex_code.lstrip('#'), end_color=hex_code.lstrip('#'), fill_type="solid")
                        ws.cell(row=row_index, column=empty_col_index).fill = fill
                    except Exception as e:
                        print(f"Ошибка при применении цвета {hex_code} в строке {row_index}: {e}")

    # Сохраняем изменения в Excel-файле
    wb.save(output_file)
    print(f"Цвета успешно применены и сохранены в файл: {output_file}")

# Пример использования
columns_with_hex = ['col_cir', 'col_sq']
current_date = datetime.now().strftime("%d_%m")
yesterday_date = datetime.now() - timedelta(days=1)
prev_d = yesterday_date.strftime("%d_%m")
output_dir = os.path.join(os.path.dirname(__file__), 'Data')
input_file = os.path.join(output_dir, f"brightness_analysis_{current_date}.xlsx")
# input_file = os.path.join(output_dir, f"brightness_analysis_{prev_d}.xlsx")
out_file_emp = os.path.join(output_dir, f"bright_analysis_{current_date}_emp.xlsx")
output_file = os.path.join(output_dir, f"bright_analysis_{current_date}_color.xlsx")
df = pd.read_excel(input_file)
df = insert_empty_columns(df,columns_with_hex)
df.to_excel(out_file_emp, index = False)
print(f"Файл c добавленными столбцами успешно сохранён: {out_file_emp}")
fill_color_columns_to_excel(output_file, df, columns_with_hex)
# fill_color_columns_to_excel(
#     input_file=input_file,
#     output_file=output_file,
#     columns_with_hex=columns_with_hex
# )
