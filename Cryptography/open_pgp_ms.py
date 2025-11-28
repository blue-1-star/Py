import os

# Правильные расширения для OpenKeychain
KEY_EXTENSIONS = ('.pgp', '.gpg', '.asc', '.bak', '.backup', '.key', '.pem')

# Задайте имя файла здесь
KEY_FILE_NAME = "my_backup.pgp"  # измените на имя вашего файла

def get_key_file_path():
    """Возвращает путь к файлу ключа в каталоге Z:\Keys"""
    keys_dir = "Z:/Keys"
    file_path = os.path.join(keys_dir, KEY_FILE_NAME)
    
    if os.path.exists(file_path):
        print(f"✅ Файл найден: {file_path}")
        return file_path
    else:
        print(f"❌ Файл не найден: {file_path}")
        print(f"📁 Проверьте каталог: {keys_dir}")
        return None

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

def analyze_key_file():
    """Анализирует файл ключа и выводит информацию о нем"""
    print("=" * 60)
    print("🔍 АНАЛИЗ ФАЙЛА КЛЮЧА")
    print("=" * 60)
    
    file_path = get_key_file_path()
    
    if not file_path:
        return None
    
    # Анализируем файл
    filename = os.path.basename(file_path)
    file_type = detect_openkeychain_file(file_path)
    size = os.path.getsize(file_path)
    
    print(f"\n📄 Файл: {filename}")
    print(f"📏 Размер: {size} байт")
    print(f"🔍 Тип: {file_type}")
    print(f"📍 Путь: {file_path}")
    
    return file_path

# 🎯 ОСНОВНАЯ ФУНКЦИЯ
def get_key_file():
    """Основная функция для получения файла ключа"""
    return get_key_file_path()

# 🚀 ИСПОЛЬЗОВАНИЕ
if __name__ == "__main__":
    key_file = get_key_file()
    
    if key_file:
        print(f"✅ Файл для обработки: {key_file}")
        # Здесь ваш код обработки файла
    else:
        print("❌ Файл не найден")