# G:\Programming\Py\SQLite\shema.py
"""
Скрипт для экспорта структуры БД osbb_test.db в текстовый файл
Файл сохраняется рядом с БД
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# ==================================================
# ПУТИ
# ==================================================

# Путь к БД
DB_PATH = Path("G:/Programming/Py/OSBB/Data/db/osbb_test.db")

# Проверяем, существует ли БД
if not DB_PATH.exists():
    print(f"❌ База данных не найдена: {DB_PATH}")
    exit(1)

# Формируем путь для выходного файла (рядом с БД)
OUTPUT_FILE = DB_PATH.parent / f"{DB_PATH.stem}_schema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# ==================================================
# ЭКСПОРТ СТРУКТУРЫ
# ==================================================

def get_foreign_keys(cursor, table_name):
    """
    Получает внешние ключи таблицы с обработкой разных версий SQLite
    """
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    fks = cursor.fetchall()
    
    result = []
    for fk in fks:
        # В разных версиях SQLite PRAGMA возвращает разное количество колонок
        if len(fk) == 7:
            # Старая версия: (id, seq, table, from, to, on_update, on_delete, match)
            # На самом деле их 7: id, seq, table, from, to, on_update, on_delete
            # Некоторые версии возвращают 8 (с match)
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
            # Новая версия или нестандартная структура
            # Пробуем определить по именам колонок
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Если не можем определить структуру, выводим как есть
            result.append({
                'raw': fk,
                'table': fk[2] if len(fk) > 2 else 'unknown',
                'from': fk[3] if len(fk) > 3 else 'unknown',
                'to': fk[4] if len(fk) > 4 else 'unknown'
            })
    
    return result


def export_schema(db_path: Path, output_file: Path):
    """Экспортирует структуру БД в текстовый файл"""
    
    # Подключаемся к БД
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Открываем файл для записи
    with open(output_file, 'w', encoding='utf-8') as f:
        # Заголовок
        f.write("="*80 + "\n")
        f.write(f"СТРУКТУРА БАЗЫ ДАННЫХ\n")
        f.write(f"Файл: {db_path.name}\n")
        f.write(f"Путь: {db_path}\n")
        f.write(f"Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # ==========================================
        # 1. ВСЕ ТАБЛИЦЫ (CREATE SQL)
        # ==========================================
        f.write("📋 ВСЕ ТАБЛИЦЫ\n")
        f.write("-"*80 + "\n\n")
        
        cursor.execute("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        
        tables = cursor.fetchall()
        
        if not tables:
            f.write("⚠️ Таблицы не найдены\n\n")
        else:
            for table_name, create_sql in tables:
                f.write(f"📌 ТАБЛИЦА: {table_name}\n")
                f.write("-"*80 + "\n")
                f.write(create_sql + "\n\n")
                
                # Получаем количество строк
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    f.write(f"📊 Строк: {row_count}\n\n")
                except:
                    f.write(f"📊 Строк: (не удалось подсчитать)\n\n")
                
                # Получаем структуру колонок через PRAGMA
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                f.write("📐 СТРУКТУРА КОЛОНОК:\n")
                f.write("-"*60 + "\n")
                f.write(f"{'CID':<6} {'NAME':<25} {'TYPE':<15} {'NOT NULL':<10} {'PK':<5}\n")
                f.write("-"*60 + "\n")
                
                for col in columns:
                    # PRAGMA table_info возвращает: cid, name, type, notnull, dflt_value, pk
                    if len(col) >= 6:
                        cid, name, col_type, notnull, dflt_value, pk = col[:6]
                        f.write(f"{cid:<6} {name:<25} {col_type:<15} {'✅' if notnull else '❌':<10} {'✅' if pk else '❌':<5}\n")
                    else:
                        f.write(f"{col}\n")
                
                # Индексы
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()
                if indexes:
                    f.write("\n🔍 ИНДЕКСЫ:\n")
                    for idx in indexes:
                        # PRAGMA index_list возвращает: seq, name, unique
                        if len(idx) >= 3:
                            seq, idx_name, unique = idx[0], idx[1], idx[2]
                            f.write(f"  - {idx_name} {'(UNIQUE)' if unique else ''}\n")
                        else:
                            f.write(f"  - {idx}\n")
                
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
        # 2. ВСЕ ПРЕДСТАВЛЕНИЯ (VIEWS)
        # ==========================================
        cursor.execute("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='view'
            ORDER BY name
        """)
        
        views = cursor.fetchall()
        
        if views:
            f.write("👁️ ПРЕДСТАВЛЕНИЯ (VIEWS)\n")
            f.write("-"*80 + "\n\n")
            
            for view_name, create_sql in views:
                f.write(f"📌 VIEW: {view_name}\n")
                f.write("-"*40 + "\n")
                f.write(create_sql + "\n\n")
        
        # ==========================================
        # 3. СВЯЗИ МЕЖДУ ТАБЛИЦАМИ (SUMMARY)
        # ==========================================
        f.write("\n" + "="*80 + "\n")
        f.write("📊 СВОДНАЯ ИНФОРМАЦИЯ\n")
        f.write("-"*80 + "\n\n")
        
        # Список всех таблиц с количеством строк
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
        
        # Общее количество таблиц
        f.write("\n" + "-"*50 + "\n")
        f.write(f"Всего таблиц: {len(tables)}\n")
        f.write(f"Всего представлений: {len(views)}\n")
        f.write(f"Всего строк: {total_rows:,}\n")
        
        # Размер БД
        db_size = db_path.stat().st_size / (1024 * 1024)
        f.write(f"Размер БД: {db_size:.2f} MB\n")
        
        # ==========================================
        # 4. ОТНОШЕНИЯ (FOREIGN KEYS)
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
    print(f"✅ Структура БД экспортирована в файл:\n   {output_file}")

# ==================================================
# ЗАПУСК
# ==================================================

if __name__ == "__main__":
    print(f"📁 База данных: {DB_PATH}")
    print(f"📄 Выходной файл: {OUTPUT_FILE}")
    print("⏳ Экспортирую структуру...")
    
    try:
        export_schema(DB_PATH, OUTPUT_FILE)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()