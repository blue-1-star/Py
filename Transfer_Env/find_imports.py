import os
import ast
import glob
from collections import defaultdict

def find_imports_in_file(filepath):
    """Найти все импорты в файле"""
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except:
        pass
    return imports

def scan_directory(directory):
    """Просканировать все Python файлы в директории"""
    all_imports = set()
    python_files = glob.glob(os.path.join(directory, '**/*.py'), recursive=True)
    
    for filepath in python_files:
        imports = find_imports_in_file(filepath)
        all_imports.update(imports)
    
    return sorted(all_imports)

# Сканируем вашу папку
# directory = r"G:\Programming\Py"
directory = r"G:\Programming\Py\Audio"
imports = scan_directory(directory)

print("=== НАЙДЕННЫЕ ИМПОРТЫ ===")
for imp in imports:
    print(imp)

print(f"\nВсего найдено: {len(imports)} библиотек")