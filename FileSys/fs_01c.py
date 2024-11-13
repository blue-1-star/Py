import os

def analyze_directory(directory_path):
    result = {}
    try:
        # Проходим по всем поддиректориям в указанной директории
        for root, dirs, files in os.walk(directory_path):
            # Берём только непосредственные поддиректории
            if root == directory_path:
                for subdir in dirs:
                    subdir_path = os.path.join(root, subdir)
                    # Считаем количество файлов в поддиректории
                    subdir_files_count = sum(len(files) for _, _, files in os.walk(subdir_path))
                    # Проверяем, есть ли вложенные поддиректории
                    has_nested_dirs = any(os.path.isdir(os.path.join(subdir_path, d)) for d in os.listdir(subdir_path))
                    result[subdir] = {
                        "files_count": subdir_files_count,
                        "has_nested_dirs": has_nested_dirs
                    }
                break
    except Exception as e:
        print(f"Ошибка при обработке директории: {e}")
    return result

# Пример использования
directory = "G:/test/"
analysis = analyze_directory(directory)
for subdir, info in analysis.items():
    print(f"Поддиректория: {subdir}, Количество файлов: {info['files_count']}, Содержит поддиректории: {info['has_nested_dirs']}")
