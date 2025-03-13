import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Функция для перевода номера месяца в название
def get_month_name(month_number):
    months = {
        1: "январь", 2: "февраль", 3: "март", 4: "апрель",
        5: "май", 6: "июнь", 7: "июль", 8: "август",
        9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
    }
    return months.get(month_number, "неизвестный месяц")

def create_report(inp_dir, excel_file, sheet_name, val_cell, txt_list, title):
    # Полный путь к файлу
    file_path = os.path.join(inp_dir, excel_file)
    
    # Чтение данных из Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Преобразование столбца 'Date' в формат datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    
    # Получение последней строки данных
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]
    
    # Извлечение месяца и года из столбца 'Date'
    date = last_row['Date']
    month = date.month
    year = date.year
    month_name = get_month_name(month)
    suffix = f"{month:02d}_{year}"
    
    # Вычисление расхода электроэнергии и воды
    el_count = last_row['El_count'] - prev_row['El_count']
    wat_count = last_row['Wat_count'] - prev_row['Wat_count']
    
    # Формирование данных для отчета
    report_data = [
        [txt_list[0], f"{last_row['El_bill']} грн", txt_list[1], f"{el_count} кВт·ч"],
        [txt_list[2], f"{last_row['water']} грн", txt_list[3], f"{wat_count} м³"],
        [txt_list[4], f"{last_row['utilities']} грн", "", ""],
        [txt_list[5], f"{last_row['TV & Internet']} грн", "", ""],
        [txt_list[6], f"{last_row['litter']} грн", "", ""],
        [txt_list[7], f"{last_row['heating']} грн", "", ""],
        [txt_list[8], f"{last_row['Total']} грн", "", ""]
    ]
    
    # Создание текстового файла
    txt_report_path = os.path.join(inp_dir, f"report_{suffix}.txt")
    with open(txt_report_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(title.replace("__", month_name).replace("____", str(year)) + "\n\n")
        txt_file.write("+----------------+----------+----------------+----------+\n")
        txt_file.write("| Показатель     | Сумма    | Показатель     | Сумма    |\n")
        txt_file.write("+----------------+----------+----------------+----------+\n")
        for row in report_data:
            line = f"| {row[0].ljust(14)} | {row[1].rjust(8)} | {row[2].ljust(14)} | {row[3].rjust(8)} |"
            txt_file.write(line + "\n")
        txt_file.write("+----------------+----------+----------------+----------+\n")
    
    # Создание PDF-файла
    pdf_report_path = os.path.join(inp_dir, f"report_{suffix}.pdf")
    
    # Регистрация шрифта с поддержкой кириллицы
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    
    doc = SimpleDocTemplate(pdf_report_path, pagesize=A4)
    elements = []
    
    # Заголовок
    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'DejaVuSans'  # Используем шрифт с поддержкой кириллицы
    elements.append(Paragraph(title.replace("__", month_name).replace("____", str(year)), styles['Title']))
    
    # Таблица с данными
    table_data = [
        ["Показатель", "Сумма", "Показатель", "Сумма"]
    ] + report_data
    
    table = Table(table_data, colWidths=[100, 80, 100, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),  # Шрифт для заголовка
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),  # Шрифт для данных
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)

# Параметры
inp_dir = r"D:\OneDrive\Документы"
excel_file = "Flat_Arn.xlsx"
sheet_name = "Push"
val_cell = ['El_bill', 'El_count', 'water', 'Wat_count', 'utilities', 'TV & Internet', 'litter', 'heating', 'Total']
txt_list = ['Свет', 'Расх ээ', 'вода', 'Расх воды', 'квартплата', 'TV', 'мусор', 'отопление', 'ВСЕГО']
title = "Коммунальные расходы за __ месяц ____ года"

# Создание отчета
create_report(inp_dir, excel_file, sheet_name, val_cell, txt_list, title)