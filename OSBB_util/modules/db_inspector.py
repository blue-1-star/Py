# G:\Programming\Py\OSBB_util\modules\db_inspector.py
"""
Модуль для инспекции структуры SQLite базы данных
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class DatabaseInspector:
    """Инспектор структуры базы данных SQLite"""
    
    def __init__(self, db_path: Path):
        """
        Args:
            db_path: путь к файлу базы данных
        """
        self.db_path = Path(db_path)
        self.connection = None
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"База данных не найдена: {self.db_path}")
    
    def get_connection(self):
        """Получает соединение с БД"""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection
    
    def close(self):
        """Закрывает соединение"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def get_all_tables(self) -> List[str]:
        """Возвращает список всех таблиц"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        return [row[0] for row in cursor.fetchall()]
    
    def get_table_info(self, table_name: str) -> Dict:
        """
        Получает полную информацию о таблице
        
        Returns:
            Dict с ключами:
                - name: имя таблицы
                - columns: список колонок
                - indexes: список индексов
                - foreign_keys: список внешних ключей
                - row_count: количество строк
                - create_sql: CREATE TABLE запрос
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Структура таблицы
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Индексы
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()
        
        # Внешние ключи
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        
        # Количество строк
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        # CREATE SQL
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        create_sql = cursor.fetchone()
        
        return {
            'name': table_name,
            'columns': columns,
            'indexes': indexes,
            'foreign_keys': foreign_keys,
            'row_count': row_count,
            'create_sql': create_sql[0] if create_sql else None
        }
    
    def get_relationships(self) -> List[Dict]:
        """
        Получает все связи между таблицами (foreign keys)
        """
        relationships = []
        
        for table_name in self.get_all_tables():
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            fks = cursor.fetchall()
            
            for fk in fks:
                if len(fk) >= 5:
                    relationships.append({
                        'source_table': table_name,
                        'source_column': fk[3] if len(fk) > 3 else 'unknown',
                        'target_table': fk[2] if len(fk) > 2 else 'unknown',
                        'target_column': fk[4] if len(fk) > 4 else 'unknown',
                        'on_update': fk[5] if len(fk) > 5 else 'NO ACTION',
                        'on_delete': fk[6] if len(fk) > 6 else 'NO ACTION'
                    })
        
        return relationships
    
    def get_schema_summary(self) -> Dict:
        """
        Получает сводную информацию о всей БД
        """
        tables = self.get_all_tables()
        total_rows = 0
        table_summary = []
        
        for table in tables:
            info = self.get_table_info(table)
            total_rows += info['row_count']
            table_summary.append({
                'name': table,
                'row_count': info['row_count'],
                'column_count': len(info['columns']),
                'has_pk': any(col[5] for col in info['columns']),  # pk = 1
                'has_fk': len(info['foreign_keys']) > 0,
                'has_indexes': len(info['indexes']) > 0
            })
        
        return {
            'db_path': str(self.db_path),
            'db_size_mb': round(self.db_path.stat().st_size / (1024 * 1024), 2),
            'table_count': len(tables),
            'total_rows': total_rows,
            'tables': table_summary,
            'relationships': self.get_relationships()
        }
    
    def export_create_sql(self, output_path: Path):
        """
        Экспортирует CREATE SQL для всех таблиц в файл
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        
        tables = cursor.fetchall()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("--" + "="*76 + "\n")
            f.write("-- ПОЛНАЯ СХЕМА БАЗЫ ДАННЫХ\n")
            f.write("--" + "="*76 + "\n")
            f.write(f"-- Файл: {self.db_path.name}\n")
            f.write(f"-- Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("--" + "="*76 + "\n\n")
            
            f.write("PRAGMA foreign_keys = OFF;\n\n")
            
            # DROP TABLE
            f.write("-- Удаление существующих таблиц\n")
            for table_name, _ in reversed(tables):
                f.write(f"DROP TABLE IF EXISTS {table_name};\n")
            f.write("\n")
            
            # CREATE TABLE
            f.write("-- Создание таблиц\n")
            for table_name, create_sql in tables:
                f.write(create_sql + ";\n\n")
            
            f.write("PRAGMA foreign_keys = ON;\n")
    
    def export_table_documentation(self, table_name: str, output_path: Path):
        """
        Экспортирует документацию по одной таблице в TXT
        """
        info = self.get_table_info(table_name)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write(f"📌 ТАБЛИЦА: {info['name']}\n")
            f.write("="*80 + "\n")
            f.write(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"📊 Строк: {info['row_count']:,}\n")
            f.write("="*80 + "\n\n")
            
            # Структура колонок
            f.write("📐 СТРУКТУРА КОЛОНОК\n")
            f.write("-"*80 + "\n")
            f.write(f"{'#':<6} {'Имя':<30} {'Тип':<20} {'NOT NULL':<12} {'PK':<5}\n")
            f.write("-"*80 + "\n")
            
            for col in info['columns']:
                if len(col) >= 6:
                    cid, name, col_type, notnull, dflt_value, pk = col[:6]
                    pk_str = "✅" if pk else ""
                    notnull_str = "✅" if notnull else "❌"
                    f.write(f"{cid:<6} {name:<30} {col_type:<20} {notnull_str:<12} {pk_str:<5}\n")
            
            f.write("\n")
            
            # Индексы
            if info['indexes']:
                f.write("🔍 ИНДЕКСЫ\n")
                f.write("-"*80 + "\n")
                for idx in info['indexes']:
                    if len(idx) >= 3:
                        f.write(f"  • {idx[1]} {'(UNIQUE)' if idx[2] else ''}\n")
            else:
                f.write("🔍 ИНДЕКСЫ: нет\n")
            
            f.write("\n")
            
            # Внешние ключи
            if info['foreign_keys']:
                f.write("🔗 ВНЕШНИЕ КЛЮЧИ\n")
                f.write("-"*80 + "\n")
                for fk in info['foreign_keys']:
                    if len(fk) >= 5:
                        f.write(f"  • {fk[3]} → {fk[2]}.{fk[4]}\n")
            else:
                f.write("🔗 ВНЕШНИЕ КЛЮЧИ: нет\n")
            
            f.write("\n")
            
            # CREATE SQL
            f.write("📝 SQL СОЗДАНИЯ\n")
            f.write("-"*80 + "\n")
            f.write(info['create_sql'] + "\n")
            
            f.write("\n" + "="*80 + "\n")