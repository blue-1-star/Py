import os

# Правильные расширения для OpenKeychain
KEY_EXTENSIONS = ('.pgp', '.gpg', '.asc', '.bak', '.backup', '.key', '.pem')

def find_backup_file():
    """Ищет файлы бэкапа с правильными расширениями"""
    search_dirs = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        "C:/Users/Public/Downloads",
        "Z:/Keys"
    ]
    
    found_files = []
    
    for directory in search_dirs:
        if os.path.exists(directory):
            print(f"🔍 Сканируем: {directory}")
            for file in os.listdir(directory):
                file_lower = file.lower()
                if any(file_lower.endswith(ext) for ext in KEY_EXTENSIONS):
                    full_path = os.path.join(directory, file)
                    found_files.append(full_path)
                    print(f"   ✅ Найден: {file}")
    
    return found_files

def detect_openkeychain_file(filepath):
    """Определяет, является ли файл бэкапом OpenKeychain"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read(500).decode('utf-8', errors='ignore')
        
        # Характерные признаки OpenKeychain файлов
        if '-----BEGIN PGP' in content:
            return "OpenPGP файл (вероятно из OpenKeychain)"
        elif 'PRIVATE KEY' in content:
            return "Приватный ключ"
        elif 'PUBLIC KEY' in content:
            return "Публичный ключ"
        else:
            return "Неизвестный формат"
            
    except Exception as e:
        return f"Ошибка чтения: {e}"

# 🎯 ОСНОВНАЯ ФУНКЦИЯ ПОИСКА
def find_openkeychain_backup():
    print("=" * 60)
    print("🔍 ПОИСК ФАЙЛОВ OPENKEYCHAIN")
    print("=" * 60)
    
    # Ищем файлы с расширениями .pgp, .gpg, .asc и т.д.
    found_files = find_backup_file()
    
    if not found_files:
        print("❌ Файлы бэкапа не найдены!")
        print("Ищем в стандартных местах:")
        for dir_path in [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop")
        ]:
            if os.path.exists(dir_path):
                print(f"📁 {dir_path}")
        return None
    
    print(f"\n✅ Найдено {len(found_files)} файлов:")
    
    # Показываем информацию о каждом файле
    for i, filepath in enumerate(found_files, 1):
        filename = os.path.basename(filepath)
        file_type = detect_openkeychain_file(filepath)
        size = os.path.getsize(filepath)
        
        print(f"\n{i}. 📄 {filename}")
        print(f"   📏 Размер: {size} байт")
        print(f"   🔍 Тип: {file_type}")
        print(f"   📍 Путь: {filepath}")
    
    # Предлагаем выбрать файл
    try:
        choice = int(input(f"\nВыберите файл (1-{len(found_files)}): ")) - 1
        if 0 <= choice < len(found_files):
            selected_file = found_files[choice]
            print(f"🎯 Выбран: {selected_file}")
            return selected_file
        else:
            print("❌ Неверный выбор")
            return None
    except ValueError:
        print("❌ Введите число")
        return None

# 🚀 АВТОМАТИЧЕСКИЙ ПОИСК .PGP ФАЙЛОВ
def find_pgp_files_specific():
    """Ищет specifically .pgp files"""
    pgp_files = []
    
    for directory in [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents")
    ]:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.lower().endswith('.pgp'):
                    full_path = os.path.join(directory, file)
                    pgp_files.append(full_path)
    
    return pgp_files

# 📋 ПОЛУЧЕНИЕ ФАЙЛА ОТ ПОЛЬЗОВАТЕЛЯ
def get_backup_file_interactive():
    """Интерактивный выбор файла"""
    print("📁 ВАРИАНТЫ ПОЛУЧЕНИЯ ФАЙЛА:")
    print("1. Автоматический поиск .pgp файлов")
    print("2. Указать путь вручную")
    print("3. Выбрать через диалоговое окно")
    
    choice = input("Ваш выбор (1-3): ")
    
    if choice == "1":
        # Автопоиск
        pgp_files = find_pgp_files_specific()
        if pgp_files:
            print("Найдены .pgp файлы:")
            for i, file in enumerate(pgp_files, 1):
                print(f"{i}. {file}")
            
            file_choice = input("Выберите файл (номер): ")
            try:
                return pgp_files[int(file_choice) - 1]
            except:
                return None
        else:
            print(".pgp файлы не найдены")
            return None
            
    elif choice == "2":
        # Ручной ввод
        while True:
            filepath = input("Введите полный путь к .pgp файлу: ").strip()
            filepath = filepath.replace('/', '\\')
            
            if os.path.exists(filepath):
                if filepath.lower().endswith('.pgp'):
                    return filepath
                else:
                    print("❌ Файл должен иметь расширение .pgp")
            else:
                print("❌ Файл не существует")
    
    elif choice == "3":
        # Диалоговое окно
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(
            title="Выберите .pgp файл бэкапа",
            filetypes=[("PGP files", "*.pgp"), ("All files", "*.*")]
        )
        return filepath
    
    return None

# 🎯 ИСПОЛЬЗОВАНИЕ
if __name__ == "__main__":
    backup_file = get_backup_file_interactive()
    
    if backup_file:
        print(f"✅ Файл для обработки: {backup_file}")
        # Здесь ваш код обработки файла
    else:
        print("❌ Файл не выбран")
