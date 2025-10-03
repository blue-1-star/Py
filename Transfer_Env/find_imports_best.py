import os
import glob
import ast
from collections import defaultdict

def analyze_python_files(directory):
    """Анализ всех Python файлов в директории"""
    imports = defaultdict(int)
    python_files = glob.glob(os.path.join(directory, '**/*.py'), recursive=True)
    
    print(f"Найдено {len(python_files)} Python файлов для анализа...")
    
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Обработка import module
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        lib_name = alias.name.split('.')[0]
                        imports[lib_name] += 1
                
                # Обработка from module import
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.level == 0:  # Только абсолютные импорты
                        lib_name = node.module.split('.')[0]
                        imports[lib_name] += 1
                        
        except SyntaxError:
            print(f"Синтаксическая ошибка в файле: {filepath}")
            continue
        except UnicodeDecodeError:
            print(f"Проблема с кодировкой в файле: {filepath}")
            continue
        except Exception as e:
            print(f"Ошибка при обработке {filepath}: {e}")
            continue
    
    # Фильтрация стандартных библиотек (опционально)
    standard_libs = {'os', 'sys', 'math', 'json', 'ast', 'glob', 'collections'}  # и т.д.
    third_party_imports = {k: v for k, v in imports.items() if k not in standard_libs}
    
    return third_party_imports

# Запуск анализа
directory = r"G:\Programming\Py"
results = analyze_python_files(directory)

print("=== ЧАСТОТА ИСПОЛЬЗОВАНИЯ СТОРОННИХ БИБЛИОТЕК ===")
for lib, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{lib}: {count} файлов")

print(f"\nВсего уникальных сторонних библиотек: {len(results)}")