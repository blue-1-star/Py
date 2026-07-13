# G:\Programming\Py\OSBB_util\Scripts\archive_docs.py
"""
Сбор всех документационных файлов (.md) в один ZIP-архив
Сохраняет структуру каталогов

Ищет:
- Все .md файлы в проекте
- Конкретные: CHANGELOG.md, MODULE.md, INSTALL.md, README.md

Использование:
    python Scripts/archive_docs.py
    python Scripts/archive_docs.py --include "*.md"
    python Scripts/archive_docs.py --names CHANGELOG.md MODULE.md
    python Scripts/archive_docs.py --exclude test_*.md
"""

import sys
from pathlib import Path
from datetime import datetime
import zipfile
import argparse
from typing import List, Set, Optional
import fnmatch

# Добавляем корень утилиты в путь
UTIL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(UTIL_ROOT))

from local_config import local_config


class DocArchiver:
    """Сборщик и архиватор документации"""
    
    # Имена файлов документации по умолчанию
    DEFAULT_DOC_NAMES = [
        'README.md',
        'CHANGELOG.md',
        'MODULE.md',
        'INSTALL.md',
        'CONTRIBUTING.md',
        'LICENSE.md',
        'API.md',
        'DOCS.md',
        'DEVELOPMENT.md',
        'DEPLOY.md',
    ]
    
    def __init__(self, root_path: Path, output_dir: Path):
        """
        Args:
            root_path: корень проекта (OSBB/)
            output_dir: куда сохранять архив
        """
        self.root_path = Path(root_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.found_files = []
        self.exclude_patterns = [
            'venv/*',
            '.venv/*',
            '__pycache__/*',
            '.git/*',
            '.idea/*',
            '.vscode/*',
            '*.egg-info/*',
            'dist/*',
            'build/*',
            '*.pyc',
        ]
        
    def should_exclude(self, file_path: Path) -> bool:
        """Проверяет, нужно ли исключить файл"""
        rel_path = file_path.relative_to(self.root_path)
        
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(str(rel_path), pattern):
                return True
        
        return False
    
    def find_files_by_name(self, names: Optional[List[str]] = None) -> List[Path]:
        """
        Находит все файлы с указанными именами
        
        Args:
            names: список имен файлов (если None - ищет все .md)
        
        Returns:
            список найденных файлов
        """
        found = []
        
        if names is None:
            # Ищем все .md файлы
            pattern = "*.md"
            for file_path in self.root_path.rglob(pattern):
                if not self.should_exclude(file_path):
                    found.append(file_path)
        else:
            # Ищем конкретные имена
            for file_path in self.root_path.rglob("*"):
                if file_path.is_file() and file_path.name in names:
                    if not self.should_exclude(file_path):
                        found.append(file_path)
        
        return sorted(found)
    
    def find_files_by_pattern(self, pattern: str) -> List[Path]:
        """
        Находит все файлы по маске
        
        Args:
            pattern: маска (например, "docs/*.md")
        
        Returns:
            список найденных файлов
        """
        found = []
        for file_path in self.root_path.rglob(pattern):
            if not self.should_exclude(file_path):
                found.append(file_path)
        return sorted(found)
    
    def create_archive(self, files: List[Path], archive_name: str = None,
                       preserve_path: bool = True) -> Path:
        """
        Создает ZIP-архив со списком файлов
        
        Args:
            files: список файлов для архивации
            archive_name: имя архива (если None - генерируется с датой)
            preserve_path: сохранять ли структуру каталогов
        
        Returns:
            путь к созданному архиву
        """
        if not files:
            print("⚠️  Нет файлов для архивации")
            return None
        
        # Имя архива
        if archive_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"docs_collection_{timestamp}.zip"
        
        archive_path = self.output_dir / archive_name
        
        print(f"\n📦 Создание архива: {archive_path}")
        print(f"📁 Файлов: {len(files)}")
        print("-" * 60)
        
        # Создаем архив
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files:
                if preserve_path:
                    # Сохраняем путь относительно корня проекта
                    arcname = file_path.relative_to(self.root_path.parent)
                    # Добавляем префикс "OSBB" к пути (чтобы было видно, откуда)
                    # arcname = Path("OSBB") / arcname
                else:
                    # Только имя файла (без путей)
                    arcname = file_path.name
                
                zipf.write(file_path, str(arcname))
                print(f"  📄 {arcname}")
        
        # Размер архива
        size = archive_path.stat().st_size
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size / (1024 * 1024):.2f} MB"
        
        print("-" * 60)
        print(f"✅ Архив создан: {archive_path}")
        print(f"📊 Размер: {size_str}")
        print(f"📁 Всего файлов: {len(files)}")
        
        return archive_path
    
    def run(self, pattern: str = None, names: List[str] = None,
            archive_name: str = None, preserve_path: bool = True):
        """
        Основной метод: поиск + архивация
        
        Args:
            pattern: маска поиска (например, "*.md")
            names: список имен файлов
            archive_name: имя архива
            preserve_path: сохранять структуру
        """
        # Поиск файлов
        if pattern:
            print(f"🔍 Поиск по маске: {pattern}")
            files = self.find_files_by_pattern(pattern)
        elif names:
            print(f"🔍 Поиск по именам: {', '.join(names)}")
            files = self.find_files_by_name(names)
        else:
            print(f"🔍 Поиск всех .md файлов")
            files = self.find_files_by_name()
        
        # Статистика
        if not files:
            print("⚠️  Файлы не найдены")
            return None
        
        print(f"\n📊 Найдено файлов: {len(files)}")
        
        # Показываем первые 10 файлов
        for f in files[:10]:
            rel_path = f.relative_to(self.root_path)
            print(f"  • {rel_path}")
        if len(files) > 10:
            print(f"  • ... и еще {len(files) - 10} файлов")
        
        # Создаем архив
        return self.create_archive(files, archive_name, preserve_path)


def main():
    parser = argparse.ArgumentParser(
        description="Сбор и архивация документационных файлов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  # Все .md файлы
  python archive_docs.py
  
  # Конкретные файлы
  python archive_docs.py --names README.md CHANGELOG.md MODULE.md
  
  # По маске
  python archive_docs.py --include "docs/*.md"
  
  # С указанием имени архива
  python archive_docs.py --archive my_docs.zip
        """
    )
    
    parser.add_argument("--include", type=str, 
                       help="Маска файлов (например, '*.md' или 'docs/*.md')")
    parser.add_argument("--names", type=str, nargs='+',
                       help="Имена файлов (README.md CHANGELOG.md)")
    parser.add_argument("--archive", type=str,
                       help="Имя архива (по умолчанию: docs_collection_YYYYMMDD_HHMMSS.zip)")
    parser.add_argument("--no-path", action="store_true",
                       help="Не сохранять структуру каталогов (только имена файлов)")
    parser.add_argument("--root", type=str,
                       help="Корневой каталог для поиска (по умолчанию: OSBB)")
    parser.add_argument("--list", action="store_true",
                       help="Только показать файлы без архивации")
    
    args = parser.parse_args()
    
    # Определяем корень
    if args.root:
        root_path = Path(args.root)
    else:
        root_path = local_config.osbb_root
    
    if not root_path.exists():
        print(f"❌ Корневой каталог не найден: {root_path}")
        sys.exit(1)
    
    # Создаем архиватор
    archiver = DocArchiver(root_path, local_config.output_dir / "docs_archive")
    
    # Только показать файлы
    if args.list:
        if args.include:
            files = archiver.find_files_by_pattern(args.include)
        elif args.names:
            files = archiver.find_files_by_name(args.names)
        else:
            files = archiver.find_files_by_name()
        
        print(f"\n📊 Найдено файлов: {len(files)}")
        for f in files[:20]:
            rel_path = f.relative_to(root_path)
            print(f"  • {rel_path}")
        if len(files) > 20:
            print(f"  • ... и еще {len(files) - 20} файлов")
        return
    
    # Запускаем архивацию
    archiver.run(
        pattern=args.include,
        names=args.names,
        archive_name=args.archive,
        preserve_path=not args.no_path
    )


if __name__ == "__main__":
    main()