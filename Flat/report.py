import pandas as pd
from openpyxl import load_workbook
from fpdf import FPDF

# Функция для обработки Excel-файла и создания отчета
def process_excel_to_pdf(excel_file, sheet_name, txt_list, excl_columns, oper_formula, pdf_file):
    # Чтение файла Excel
    workbook = load_workbook(excel_file)
    sheet = workbook[sheet_name]

    # Получение имен столбцов
    columns = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]

    # Получение последней строки
    last_row = sheet.max_row
    last_row_values = [cell.value for cell in sheet[last_row]]

    # Формирование словаря NameCol_TXT
    name_col_txt = {columns[i]: txt_list[i] for i in range(len(columns)) if i < len(txt_list)}

    # Формирование отчета
    report_lines = []
    for col_name, col_value in zip(columns, last_row_values):
        if col_name in excl_columns:
            prev_row = last_row - 1
            report_lines.append(f"{name_col_txt.get(col_name, col_name)}: =({col_name}{last_row}-{col_name}{prev_row})")
        else:
            report_lines.append(f"{name_col_txt.get(col_name, col_name)}: {col_value}")

    # Создание PDF-отчета
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Отчет", ln=True, align='C')
    pdf.ln(10)

    for line in report_lines:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(pdf_file)
    print(f"PDF отчет сохранен в {pdf_file}")

# Пример использования
if __name__ == "__main__":
    inp_dir = r"D:\OneDrive\Документы" 
    excel_file = "Flat_Arn.xlsx"
    file_path = os.path.join(inp_dir, excel_file)
    sheet_name = "Push"

    txt_list = ["txt1", "txt2", "txt3", "txt4"]  # Пример списка TXT
    txt_list = ['Дата','Расх воды','Расх ээ','вода','ээ']
    excl_columns = ["col1", "col2"]  # Пример исключенных столбцов
    oper_formula = "=({}{}-{}{})"  # Формула разности значений текущей и предыдущей строки
    pdf_file = "report.pdf"

    process_excel_to_pdf(file_path, sheet_name, txt_list, excl_columns, oper_formula, pdf_file)
