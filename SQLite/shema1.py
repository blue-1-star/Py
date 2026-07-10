# G:\Programming\Py\SQLite\shema.py
"""
Скрипт для экспорта структуры БД osbb_test.db в:
1. Текстовый файл (.txt) - для чтения человеком
2. SQL файл (.sql) - для восстановления структуры

Файлы сохраняются рядом с БД
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import re

# ==================================================
# ПУТИ
# ==================================================

# Путь к БД
DB_PATH = Path("G:/Programming/Py/OSBB/Data/db/osbb_test.db")

# Проверяем, существует ли БД
if not DB_PATH.exists():
    print(f"❌ База данных не найдена: {DB_PATH}")
    exit(1)

# Формируем базовое имя файла
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BASE_NAME = f"{DB_PATH.stem}_schema_{TIMESTAMP}"

# Пути для выходных файлов (рядом с БД)
OUTPUT_TXT = DB_PATH.parent / f"{BASE_NAME}.txt"
OUTPUT_SQL = DB_PATH.parent / f"{BASE_NAME}.sql"

# ==================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С FOREIGN KEYS
# ==================================================

def get_foreign_keys(cursor, table_name):
    """
    Получает внешние ключи таблицы с обработкой разных версий SQLite
    """
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    fks = cursor.fetchall()
    
    result = []
    for fk in fks:
        if len(fk) >= 7:
            result.append({
                'id': fk[0],
                'seq': fk[1],
                'table': fk[2],
                'from': fk[3],
                'to': fk[4],
                'on_update': fk[5] if len(fk) > 5 else 'NO ACTION',
                'on_delete': fk[6] if len(fk) > 6 else 'NO ACTION'
            })
        else:
            result.append({
                'raw': fk,
                'table': fk[2] if len(fk) > 2 else 'unknown',
                'from': fk[3] if len(fk) > 3 else 'unknown',
                'to': fk[4] if len(fk) > 4 else 'unknown'
            })
    
    return result

def get_all_tables(cursor):
    """Получает список всех таблиц"""
    cursor.execute("""
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='table' 
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    return cursor.fetchall()

def get_all_views(cursor):
    """Получает список всех представлений"""
    cursor.execute("""
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='view'
        ORDER BY name
    """)
    return cursor.fetchall()

def get_all_indexes(cursor):
    """Получает список всех индексов"""
    cursor.execute("""
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='index' 
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    return cursor.fetchall()

def get_all_triggers(cursor):
    """Получает список всех триггеров"""
    cursor.execute("""
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='trigger'
        ORDER BY name
    """)
    return cursor.fetchall()

# ==================================================
# ЭКСПОРТ В ТЕКСТОВЫЙ ФАЙЛ (.txt)
# ==================================================

def export_txt(db_path: Path, output_file: Path):
    """Экспортирует структуру БД в текстовый файл (для чтения человеком)"""
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Получаем все данные
    tables = get_all_tables(cursor)
    views = get_all_views(cursor)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Заголовок
        f.write("="*80 + "\n")
        f.write(f"СТРУКТУРА БАЗЫ ДАННЫХ\n")
        f.write(f"Файл: {db_path.name}\n")
        f.write(f"Путь: {db_path}\n")
        f.write(f"Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # ==========================================
        # 1. ВСЕ ТАБЛИЦЫ
        # ==========================================
        f.write("📋 ВСЕ ТАБЛИЦЫ\n")
        f.write("-"*80 + "\n\n")
        
        if not tables:
            f.write("⚠️ Таблицы не найдены\n\n")
        else:
            for table_name, create_sql in tables:
                f.write(f"📌 ТАБЛИЦА: {table_name}\n")
                f.write("-"*80 + "\n")
                f.write(create_sql + "\n\n")
                
                # Количество строк
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    f.write(f"📊 Строк: {row_count}\n\n")
                except:
                    f.write(f"📊 Строк: (не удалось подсчитать)\n\n")
                
                # Структура колонок
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                f.write("📐 СТРУКТУРА КОЛОНОК:\n")
                f.write("-"*60 + "\n")
                f.write(f"{'CID':<6} {'NAME':<25} {'TYPE':<15} {'NOT NULL':<10} {'PK':<5}\n")
                f.write("-"*60 + "\n")
                
                for col in columns:
                    if len(col) >= 6:
                        cid, name, col_type, notnull, dflt_value, pk = col[:6]
                        f.write(f"{cid:<6} {name:<25} {col_type:<15} {'✅' if notnull else '❌':<10} {'✅' if pk else '❌':<5}\n")
                
                # Индексы
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()
                if indexes:
                    f.write("\n🔍 ИНДЕКСЫ:\n")
                    for idx in indexes:
                        if len(idx) >= 3:
                            seq, idx_name, unique = idx[0], idx[1], idx[2]
                            f.write(f"  - {idx_name} {'(UNIQUE)' if unique else ''}\n")
                
                # Внешние ключи
                fks = get_foreign_keys(cursor, table_name)
                if fks:
                    f.write("\n🔗 ВНЕШНИЕ КЛЮЧИ:\n")
                    for fk in fks:
                        if 'table' in fk:
                            f.write(f"  - {fk['from']} → {fk['table']}.{fk['to']}\n")
                        else:
                            f.write(f"  - {fk}\n")
                
                f.write("\n" + "="*80 + "\n\n")
        
        # ==========================================
        # 2. VIEWS
        # ==========================================
        if views:
            f.write("👁️ ПРЕДСТАВЛЕНИЯ (VIEWS)\n")
            f.write("-"*80 + "\n\n")
            
            for view_name, create_sql in views:
                f.write(f"📌 VIEW: {view_name}\n")
                f.write("-"*40 + "\n")
                f.write(create_sql + "\n\n")
        
        # ==========================================
        # 3. СВОДНАЯ ИНФОРМАЦИЯ
        # ==========================================
        f.write("\n" + "="*80 + "\n")
        f.write("📊 СВОДНАЯ ИНФОРМАЦИЯ\n")
        f.write("-"*80 + "\n\n")
        
        f.write("📋 СПИСОК ВСЕХ ТАБЛИЦ:\n")
        f.write("-"*50 + "\n")
        f.write(f"{'#':<4} {'TABLE NAME':<35} {'ROWS':<12}\n")
        f.write("-"*50 + "\n")
        
        total_rows = 0
        for idx, (table_name, _) in enumerate(tables, 1):
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                total_rows += row_count
                f.write(f"{idx:<4} {table_name:<35} {row_count:>10,}\n")
            except:
                f.write(f"{idx:<4} {table_name:<35} {'ошибка':>10}\n")
        
        f.write("\n" + "-"*50 + "\n")
        f.write(f"Всего таблиц: {len(tables)}\n")
        f.write(f"Всего представлений: {len(views)}\n")
        f.write(f"Всего строк: {total_rows:,}\n")
        
        db_size = db_path.stat().st_size / (1024 * 1024)
        f.write(f"Размер БД: {db_size:.2f} MB\n")
        
        # ==========================================
        # 4. СВЯЗИ
        # ==========================================
        f.write("\n" + "="*80 + "\n")
        f.write("🔗 ВСЕ СВЯЗИ МЕЖДУ ТАБЛИЦАМИ\n")
        f.write("-"*80 + "\n\n")
        
        has_relations = False
        for table_name, _ in tables:
            fks = get_foreign_keys(cursor, table_name)
            
            if fks:
                has_relations = True
                f.write(f"📌 {table_name}\n")
                for fk in fks:
                    if 'table' in fk:
                        f.write(f"  - {fk['from']} → {fk['table']}.{fk['to']}\n")
                    else:
                        f.write(f"  - {fk}\n")
                f.write("\n")
        
        if not has_relations:
            f.write("⚠️ Внешние ключи (связи) не найдены\n")
    
    conn.close()
    print(f"✅ TXT файл создан: {output_file}")

# ==================================================
# ЭКСПОРТ В SQL ФАЙЛ (.sql)
# ==================================================

def export_sql(db_path: Path, output_file: Path):
    """
    Экспортирует структуру БД в SQL файл для восстановления
    Создает полный скрипт: DROP TABLE + CREATE TABLE + индексы + триггеры
    """
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Получаем все данные
    tables = get_all_tables(cursor)
    views = get_all_views(cursor)
    indexes = get_all_indexes(cursor)
    triggers = get_all_triggers(cursor)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Заголовок
        f.write("="*80 + "\n")
        f.write("-- СТРУКТУРА БАЗЫ ДАННЫХ (SQL для восстановления)\n")
        f.write(f"-- Файл: {db_path.name}\n")
        f.write(f"-- Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # Настройки для восстановления
        f.write("-- Включаем поддержку внешних ключей\n")
        f.write("PRAGMA foreign_keys = OFF;\n\n")
        
        # ==========================================
        # 1. DROP TABLE (каскадное удаление)
        # ==========================================
        f.write("-- ==========================================\n")
        f.write("-- УДАЛЕНИЕ СУЩЕСТВУЮЩИХ ТАБЛИЦ (каскадное)\n")
        f.write("-- ==========================================\n\n")
        
        # Удаляем в обратном порядке (чтобы не нарушать зависимости)
        for table_name, _ in reversed(tables):
            f.write(f"DROP TABLE IF EXISTS {table_name};\n")
        
        # ==========================================
        # 2. CREATE TABLE
        # ==========================================
        f.write("\n-- ==========================================\n")
        f.write("-- СОЗДАНИЕ ТАБЛИЦ\n")
        f.write("-- ==========================================\n\n")
        
        for table_name, create_sql in tables:
            f.write(f"-- Таблица: {table_name}\n")
            f.write(create_sql + ";\n\n")
        
        # ==========================================
        # 3. VIEWS
        # ==========================================
        if views:
            f.write("-- ==========================================\n")
            f.write("-- ПРЕДСТАВЛЕНИЯ (VIEWS)\n")
            f.write("-- ==========================================\n\n")
            
            for view_name, create_sql in views:
                f.write(f"-- View: {view_name}\n")
                f.write(create_sql + ";\n\n")
        
        # ==========================================
        # 4. ИНДЕКСЫ
        # ==========================================
        if indexes:
            f.write("-- ==========================================\n")
            f.write("-- ИНДЕКСЫ\n")
            f.write("-- ==========================================\n\n")
            
            for idx_name, create_sql in indexes:
                f.write(f"-- Индекс: {idx_name}\n")
                f.write(create_sql + ";\n\n")
        
        # ==========================================
        # 5. ТРИГГЕРЫ
        # ==========================================
        if triggers:
            f.write("-- ==========================================\n")
            f.write("-- ТРИГГЕРЫ\n")
            f.write("-- ==========================================\n\n")
            
            for trig_name, create_sql in triggers:
                f.write(f"-- Триггер: {trig_name}\n")
                f.write(create_sql + ";\n\n")
        
        # ==========================================
        # 6. ВОССТАНОВЛЕНИЕ НАСТРОЕК
        # ==========================================
        f.write("-- ==========================================\n")
        f.write("-- ВОССТАНОВЛЕНИЕ НАСТРОЕК\n")
        f.write("-- ==========================================\n\n")
        f.write("PRAGMA foreign_keys = ON;\n")
        f.write("PRAGMA quick_check;\n")
        
        # ==========================================
        # 7. КОММЕНТАРИЙ С ИНФОРМАЦИЕЙ
        # ==========================================
        f.write("\n-- ==========================================\n")
        f.write("-- ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ\n")
        f.write("-- ==========================================\n\n")
        
        f.write(f"-- Всего таблиц: {len(tables)}\n")
        f.write(f"-- Всего представлений: {len(views)}\n")
        f.write(f"-- Всего индексов: {len(indexes)}\n")
        f.write(f"-- Всего триггеров: {len(triggers)}\n")
        
        db_size = db_path.stat().st_size / (1024 * 1024)
        f.write(f"-- Размер БД: {db_size:.2f} MB\n")
        
        f.write(f"\n-- Восстановите БД командой:\n")
        f.write(f"-- sqlite3 new_database.db < {output_file.name}\n")
    
    conn.close()
    print(f"✅ SQL файл создан: {output_file}")

# ==================================================
# ОСНОВНАЯ ФУНКЦИЯ
# ==================================================

def export_schema(db_path: Path, txt_file: Path, sql_file: Path):
    """
    Экспортирует структуру БД в два файла: TXT и SQL
    """
    try:
        print("⏳ Экспортирую в TXT файл...")
        export_txt(db_path, txt_file)
        
        print("⏳ Экспортирую в SQL файл...")
        export_sql(db_path, sql_file)
        
        print("\n" + "="*60)
        print("✅ ГОТОВО!")
        print(f"📄 TXT файл: {txt_file}")
        print(f"📄 SQL файл: {sql_file}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

# ==================================================
# ЗАПУСК
# ==================================================

if __name__ == "__main__":
    print("="*60)
    print("ЭКСПОРТ СТРУКТУРЫ БАЗЫ ДАННЫХ")
    print("="*60)
    print(f"📁 База данных: {DB_PATH}")
    print(f"📄 TXT файл: {OUTPUT_TXT}")
    print(f"📄 SQL файл: {OUTPUT_SQL}")
    print("="*60 + "\n")
    
    export_schema(DB_PATH, OUTPUT_TXT, OUTPUT_SQL)