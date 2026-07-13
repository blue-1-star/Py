# G:\Programming\Py\OSBB_util\Scripts\export_db_schema.py
"""
Экспорт структуры базы данных osbb_test.db
Сохраняет в output/02_database/
"""

import sys
from pathlib import Path
from datetime import datetime

# Добавляем корень утилиты в путь
UTIL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(UTIL_ROOT))

from local_config import local_config
from modules.db_inspector import DatabaseInspector


def main():
    print("=" * 60)
    print("🗄️ ЭКСПОРТ СТРУКТУРЫ БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    # Путь к БД
    db_path = local_config.db_test
    print(f"📁 База данных: {db_path}")
    
    if not db_path.exists():
        print(f"❌ Ошибка: База данных не найдена: {db_path}")
        return
    
    # Создаем инспектор
    inspector = DatabaseInspector(db_path)
    
    # Создаем выходные директории
    db_dir = local_config.db_dir
    tables_dir = local_config.tables_dir
    db_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Целевой каталог: {db_dir}")
    print("-" * 60)
    
    # ==========================================
    # 1. Полная схема (SQL)
    # ==========================================
    print("⏳ Экспорт полной схемы (SQL)...")
    sql_file = db_dir / "schema_full.sql"
    inspector.export_create_sql(sql_file)
    print(f"  ✅ {sql_file.name}")
    
    # ==========================================
    # 2. Сводная информация
    # ==========================================
    print("⏳ Сбор сводной информации...")
    summary = inspector.get_schema_summary()
    
    # Сохраняем сводку в TXT
    summary_file = db_dir / "schema_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("📊 СВОДНАЯ ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ\n")
        f.write("="*80 + "\n")
        f.write(f"Файл:    {summary['db_path']}\n")
        f.write(f"Размер:  {summary['db_size_mb']} MB\n")
        f.write(f"Таблиц:  {summary['table_count']}\n")
        f.write(f"Строк:   {summary['total_rows']:,}\n")
        f.write("="*80 + "\n\n")
        
        f.write("📋 СПИСОК ТАБЛИЦ\n")
        f.write("-"*80 + "\n")
        f.write(f"{'#':<4} {'Имя':<30} {'Строк':<12} {'Колонок':<10} {'PK':<5} {'FK':<5}\n")
        f.write("-"*80 + "\n")
        
        for i, table in enumerate(summary['tables'], 1):
            f.write(f"{i:<4} {table['name']:<30} {table['row_count']:>10,}  "
                   f"{table['column_count']:<10} {'✅' if table['has_pk'] else '❌':<5} "
                   f"{'✅' if table['has_fk'] else '❌':<5}\n")
        
        # Связи
        if summary['relationships']:
            f.write("\n🔗 СВЯЗИ МЕЖДУ ТАБЛИЦАМИ\n")
            f.write("-"*80 + "\n")
            for rel in summary['relationships']:
                f.write(f"  • {rel['source_table']}.{rel['source_column']} → "
                       f"{rel['target_table']}.{rel['target_column']}\n")
    
    print(f"  ✅ {summary_file.name}")
    
    # ==========================================
    # 3. Документация по каждой таблице
    # ==========================================
    print("\n⏳ Экспорт документации по таблицам...")
    
    tables = inspector.get_all_tables()
    for i, table_name in enumerate(tables, 1):
        doc_file = tables_dir / f"{table_name}.txt"
        inspector.export_table_documentation(table_name, doc_file)
        print(f"  {i:>3}. ✅ {table_name}.txt")
    
    # ==========================================
    # 4. Связи (отдельный файл)
    # ==========================================
    relationships = inspector.get_relationships()
    if relationships:
        rel_file = db_dir / "relationships.txt"
        with open(rel_file, 'w', encoding='utf-8') as f:
            f.write("🔗 СВЯЗИ МЕЖДУ ТАБЛИЦАМИ\n")
            f.write("="*80 + "\n\n")
            for rel in relationships:
                f.write(f"  • {rel['source_table']}.{rel['source_column']} → "
                       f"{rel['target_table']}.{rel['target_column']}\n")
                if 'on_update' in rel:
                    f.write(f"      ON UPDATE: {rel['on_update']}, ON DELETE: {rel['on_delete']}\n")
        print(f"  ✅ relationships.txt")
    
    # ==========================================
    # 5. Закрываем соединение
    # ==========================================
    inspector.close()
    
    print("\n" + "=" * 60)
    print("✅ ГОТОВО!")
    print(f"📄 Результаты в: {db_dir}")
    print(f"📄 Документация таблиц: {tables_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()