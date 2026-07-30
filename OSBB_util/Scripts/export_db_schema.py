#!/usr/bin/env python
"""
Модуль для экспорта структуры базы данных.
Может использоваться как самостоятельный скрипт или импортироваться.

Пример запуска из командной строки:
  python export_db_schema.py --db G:/Programming/OSBB_cl/data/db/osbb_test.db --output ./snapshots

Пример импорта в другой модуль:
  from export_db_schema import export_db_schema
  export_db_schema(db_path=Path("..."), snapshots_root=Path("..."))
"""

import sys
import argparse
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional

# ==========================================
# КОНФИГУРАЦИЯ (по умолчанию)
# ==========================================

DEFAULT_DB = Path("G:/Programming/OSBB_cl/data/db/osbb_test.db")
DEFAULT_SNAPSHOTS_DIR = Path("G:/Programming/Py/OSBB_util/snapshots")


# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

def get_project_name(db_path: Path) -> str:
    """Возвращает имя проекта по пути к БД (берём родительскую папку ../.. )"""
    return db_path.parent.parent.name


def get_snapshot_dir(db_path: Path, snapshots_root: Path) -> Path:
    """Формирует путь к каталогу снимка с датой"""
    project_name = get_project_name(db_path)
    date_str = datetime.now().strftime("%Y_%m_%d")
    return snapshots_root / f"{date_str}_{project_name}"


# ==========================================
# ОСНОВНАЯ ЛОГИКА
# ==========================================

def get_table_list(conn: sqlite3.Connection) -> list[str]:
    """Возвращает список всех таблиц (кроме системных)"""
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    return [row[0] for row in cur.fetchall()]


def get_table_schema(conn: sqlite3.Connection, table_name: str) -> str:
    """Возвращает CREATE TABLE для таблицы"""
    cur = conn.cursor()
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    row = cur.fetchone()
    return row[0] if row else f"-- Таблица {table_name} не найдена"


def get_table_info(conn: sqlite3.Connection, table_name: str) -> list:
    """Возвращает структуру таблицы (PRAGMA table_info)"""
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    return cur.fetchall()


def get_row_count(conn: sqlite3.Connection, table_name: str) -> int:
    """Возвращает количество строк в таблице"""
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cur.fetchone()[0]


def export_db_schema(
    db_path: Path,
    snapshots_root: Optional[Path] = None,
    include_data_sample: bool = False,
    limit_sample: int = 5,
) -> Path:
    """
    Экспортирует структуру базы данных в папку с датой внутри snapshots/.
    
    Args:
        db_path: путь к файлу базы данных
        snapshots_root: корневой каталог для снимков (по умолчанию snapshots/)
        include_data_sample: включить примеры данных
        limit_sample: количество строк в примере
    
    Returns:
        Path: путь к созданному каталогу снимка
    """
    if snapshots_root is None:
        snapshots_root = DEFAULT_SNAPSHOTS_DIR
    
    output_dir = get_snapshot_dir(db_path, snapshots_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Подкаталог для таблиц
    tables_dir = output_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    
    # 1. Полная схема (SQL)
    sql_file = output_dir / "schema_full.sql"
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write("--" + "="*76 + "\n")
        f.write("-- ПОЛНАЯ СХЕМА БАЗЫ ДАННЫХ\n")
        f.write("--" + "="*76 + "\n")
        f.write(f"-- Файл: {db_path.name}\n")
        f.write(f"-- Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("--" + "="*76 + "\n\n")
        
        f.write("PRAGMA foreign_keys = OFF;\n\n")
        
        tables = get_table_list(conn)
        
        # DROP TABLE
        f.write("-- Удаление существующих таблиц\n")
        for table in reversed(tables):
            f.write(f"DROP TABLE IF EXISTS {table};\n")
        f.write("\n")
        
        # CREATE TABLE
        f.write("-- Создание таблиц\n")
        for table in tables:
            create_sql = get_table_schema(conn, table)
            f.write(create_sql + ";\n\n")
        
        f.write("PRAGMA foreign_keys = ON;\n")
    
    print(f"  ✅ schema_full.sql")
    
    # 2. Сводная информация
    summary_file = output_dir / "schema_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("📊 СВОДНАЯ ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ\n")
        f.write("="*80 + "\n")
        f.write(f"Файл:    {db_path.name}\n")
        f.write(f"Размер:  {db_path.stat().st_size / (1024*1024):.2f} MB\n")
        f.write(f"Таблиц:  {len(tables)}\n")
        f.write("="*80 + "\n\n")
        
        f.write("📋 СПИСОК ТАБЛИЦ\n")
        f.write("-"*80 + "\n")
        f.write(f"{'#':<4} {'Имя':<35} {'Строк':<12} {'Колонок':<10}\n")
        f.write("-"*80 + "\n")
        
        total_rows = 0
        for i, table in enumerate(tables, 1):
            columns = get_table_info(conn, table)
            row_count = get_row_count(conn, table)
            total_rows += row_count
            f.write(f"{i:<4} {table:<35} {row_count:>10,}  {len(columns):<10}\n")
        
        f.write("\n" + "-"*80 + "\n")
        f.write(f"Всего таблиц: {len(tables)}\n")
        f.write(f"Всего строк:  {total_rows:,}\n")
    
    print(f"  ✅ schema_summary.txt")
    
    # 3. Документация по каждой таблице
    print("  📄 Документация таблиц:")
    for table in tables:
        doc_file = tables_dir / f"{table}.txt"
        columns = get_table_info(conn, table)
        row_count = get_row_count(conn, table)
        
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write(f"📌 ТАБЛИЦА: {table}\n")
            f.write("="*80 + "\n")
            f.write(f"📊 Строк: {row_count:,}\n")
            f.write("="*80 + "\n\n")
            
            f.write("📐 СТРУКТУРА КОЛОНОК\n")
            f.write("-"*80 + "\n")
            f.write(f"{'#':<6} {'Имя':<30} {'Тип':<20} {'NOT NULL':<12} {'PK':<5}\n")
            f.write("-"*80 + "\n")
            
            for col in columns:
                cid, name, col_type, notnull, dflt_value, pk = col[:6]
                pk_str = "✅" if pk else ""
                notnull_str = "✅" if notnull else "❌"
                f.write(f"{cid:<6} {name:<30} {col_type:<20} {notnull_str:<12} {pk_str:<5}\n")
            
            # Пример данных
            if include_data_sample and row_count > 0:
                f.write("\n📊 ПРИМЕР ДАННЫХ (первые {limit_sample} строк)\n")
                f.write("-"*80 + "\n")
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM {table} LIMIT {limit_sample}")
                sample_rows = cur.fetchall()
                if sample_rows:
                    # Заголовки
                    headers = [desc[0] for desc in cur.description] if cur.description else []
                    if headers:
                        f.write(" | ".join(h for h in headers) + "\n")
                        f.write("-"*80 + "\n")
                        for row in sample_rows:
                            f.write(" | ".join(str(v) for v in row) + "\n")
        
        print(f"    ✅ {table}.txt")
    
    conn.close()
    return output_dir


# ==========================================
# КОМАНДНАЯ СТРОКА
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="Экспорт структуры базы данных")
    parser.add_argument("--db", type=str, default=str(DEFAULT_DB),
                       help="Путь к файлу БД")
    parser.add_argument("--snapshots", type=str, default=str(DEFAULT_SNAPSHOTS_DIR),
                       help="Корневой каталог для снимков")
    parser.add_argument("--sample", action="store_true",
                       help="Включить примеры данных")
    parser.add_argument("--limit", type=int, default=5,
                       help="Количество строк в примере")
    
    args = parser.parse_args()
    
    db_path = Path(args.db)
    snapshots_root = Path(args.snapshots)
    
    if not db_path.exists():
        print(f"❌ Ошибка: база данных не найдена: {db_path}")
        sys.exit(1)
    
    print(f"🗄️ Экспорт структуры БД")
    print(f"📁 БД: {db_path}")
    print(f"📁 Снимок: {get_snapshot_dir(db_path, snapshots_root)}")
    print("-" * 40)
    
    export_db_schema(
        db_path=db_path,
        snapshots_root=snapshots_root,
        include_data_sample=args.sample,
        limit_sample=args.limit,
    )
    
    print("-" * 40)
    print("✅ Готово!")


if __name__ == "__main__":
    main()