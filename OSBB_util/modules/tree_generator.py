# G:\Programming\Py\OSBB_util\modules\tree_generator.py
"""
Модуль для генерации деревьев каталогов
"""

from pathlib import Path
from datetime import datetime
from typing import List, Optional


class TreeGenerator:
    """Генератор деревьев каталогов"""
    
    EXCLUDE_DIRS = [
        '__pycache__', '.git', '.venv', 'venv', 'env',
        '.idea', '.vscode', 'node_modules', 'dist', 'build',
        '*.egg-info', '.pytest_cache', '.mypy_cache'
    ]
    
    EXCLUDE_FILES = [
        '*.pyc', '*.pyo', '*.so', '*.dll', '*.dylib',
        '.DS_Store', 'Thumbs.db'
    ]
    
    def __init__(self, root_path: Path, output_dir: Path):
        self.root = root_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def should_exclude(self, path: Path) -> bool:
        """Проверяет, нужно ли исключить путь"""
        name = path.name
        
        if path.is_dir():
            for pattern in self.EXCLUDE_DIRS:
                if pattern.startswith('*'):
                    if name.endswith(pattern[1:]):
                        return True
                elif pattern == name:
                    return True
            if name.startswith('.') and name not in ['.git']:
                return True
        
        if path.is_file():
            for pattern in self.EXCLUDE_FILES:
                if pattern.startswith('*'):
                    if name.endswith(pattern[1:]):
                        return True
                elif pattern == name:
                    return True
        
        return False
    
    def generate_tree_string(self, path: Path, prefix: str = "", 
                             depth: int = 0, max_depth: Optional[int] = None,
                             show_size: bool = True, show_date: bool = True) -> str:
        """Генерирует строку с деревом"""
        
        if not path.exists() or not path.is_dir():
            return ""
        
        if max_depth is not None and depth > max_depth:
            return ""
        
        lines = []
        
        try:
            items = sorted(path.iterdir())
        except PermissionError:
            return f"{prefix}└── [Нет доступа]\n"
        
        filtered = [item for item in items if not self.should_exclude(item)]
        
        for i, item in enumerate(filtered):
            is_last = i == len(filtered) - 1
            connector = "└── " if is_last else "├── "
            next_prefix = prefix + ("    " if is_last else "│   ")
            
            line = f"{prefix}{connector}{item.name}"
            
            if item.is_file() and show_size:
                size = item.stat().st_size
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):.2f} MB"
                line += f" [{size_str}]"
                
                if show_date:
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    line += f" {mtime.strftime('%Y-%m-%d %H:%M')}"
            
            elif item.is_dir():
                line += "/"
            
            lines.append(line)
            
            if item.is_dir() and (max_depth is None or depth + 1 <= max_depth):
                sub_tree = self.generate_tree_string(
                    item, next_prefix, depth + 1,
                    max_depth, show_size, show_date
                )
                if sub_tree:
                    lines.append(sub_tree.rstrip('\n'))
        
        return '\n'.join(lines)
    
    def save_tree(self, content: str, filename: str):
        """Сохраняет дерево в файл"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {filename}")
    
    def generate_full_tree(self):
        """Полное дерево"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header = f"""
{'='*80}
ДЕРЕВО КАТАЛОГОВ ПРОЕКТА OSBB
{'='*80}
Корень:     {self.root}
Дата:       {timestamp}
Глубина:    без ограничений
Размер:     показан
Дата:       показана
{'='*80}

"""
        tree = self.generate_tree_string(self.root, show_size=True, show_date=True)
        content = header + tree
        
        self.save_tree(content, "tree_full.txt")
        
        # Сохраняем в архив
        archive_dir = self.output_dir.parent / "06_archive" / datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        self.save_tree(content, archive_dir / "tree_full.txt")
    
    def generate_limited_tree(self):
        """Ограниченное дерево (без размеров и дат)"""
        tree = self.generate_tree_string(self.root, show_size=False, show_date=False)
        self.save_tree(tree, "tree_limited.txt")
    
    def generate_by_depth(self, max_depth: int):
        """Дерево с ограничением по глубине"""
        tree = self.generate_tree_string(self.root, max_depth=max_depth, 
                                         show_size=True, show_date=True)
        self.save_tree(tree, f"tree_depth_{max_depth}.txt")