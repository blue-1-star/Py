#!/usr/bin/env python
"""
Экспорт данных из payments в Excel.
Номер авто берётся из vehicles, source_ref или comment.
"""

import sys
from pathlib import Path
import sqlite3
import pandas as pd
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from config import paths, USE_TEST_DB
except ImportError:
    PROJECT_ROOT = Path("G:/Programming/OSBB_cl")
    DB_PATH = PROJECT_ROOT / "Data" / "db" / "osbb_test.db"
    USE_TEST_DB = True


def get_db_path():
    try:
        return paths.OSBB_TEST_DB_FILE if USE_TEST_DB else paths.OSBB_DB_FILE
    except NameError:
        return DB_PATH


def export_payments_to_excel(output_file: Path = None):
    db_path = get_db_path()
    
    if not db_path.exists():
        print(f"❌ База данных не найдена: {db_path}")
        return False
    
    print(f"📁 БД: {db_path}")
    
    conn = sqlite3.connect(str(db_path))
    
    sql = """
        SELECT 
            p.payment_date AS Дата_платежа,
            p.period_code AS Период,
            p.apartment_number AS Квартира,
            p.vehicle_id AS ID_авто,
            COALESCE(
                v.license_plate_normalized,
                p.source_ref,
                p.comment,
                '—'
            ) AS Номер_авто,
            p.amount AS Сумма,
            p.base_service_code AS Услуга,
            p.payment_method AS Способ_оплаты,
            p.cashbox_code AS Касса,
            p.operator_id AS Оператор,
            p.comment AS Комментарий,
            p.created_at AS Дата_создания,
            p.id AS ID_платежа,
            p.cashier_receipt_id AS ID_квитанции,
            p.source_ref AS Источник
        FROM payments p
        LEFT JOIN vehicles v ON v.id = p.vehicle_id
        ORDER BY p.payment_date DESC, p.id DESC
    """
    
    df = pd.read_sql_query(sql, conn)
    conn.close()
    
    if df.empty:
        print("⚠️ Нет данных для экспорта")
        return False
    
    print(f"📊 Найдено записей: {len(df)}")
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path.cwd() / f"payments_export_{timestamp}.xlsx"
    
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Платежи', index=False)
        
        worksheet = writer.sheets['Платежи']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 40)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"✅ Файл сохранён: {output_file}")
    print(f"📄 Размер: {output_file.stat().st_size / 1024:.1f} KB")
    
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Экспорт платежей в Excel")
    parser.add_argument("--output", type=str, help="Путь к выходному файлу")
    parser.add_argument("--db", type=str, help="Путь к БД (если не через config)")
    
    args = parser.parse_args()
    
    if args.db:
        global DB_PATH
        DB_PATH = Path(args.db)
    
    output_file = Path(args.output) if args.output else None
    
    export_payments_to_excel(output_file)


if __name__ == "__main__":
    main()