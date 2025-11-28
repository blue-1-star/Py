import os
import subprocess
import getpass

# Задайте имя файла здесь
KEY_FILE_NAME = "backup_2025-11-23.sec.pgp"  # измените на имя вашего файла

def get_key_file():
    """Возвращает путь к файлу ключа в каталоге Z:\Keys"""
    keys_dir = "Z:/Keys"
    file_path = os.path.join(keys_dir, KEY_FILE_NAME)
    
    if os.path.exists(file_path):
        print(f"✅ Файл найден: {file_path}")
        return file_path
    else:
        print(f"❌ Файл не найден: {file_path}")
        return None

def extract_private_key(backup_file, output_file=None):
    """
    Извлекает приватный ключ из зашифрованного бэкапа OpenKeychain
    
    Args:
        backup_file: путь к зашифрованному .pgp файлу
        output_file: путь для сохранения извлеченного ключа (опционально)
    
    Returns:
        str: путь к извлеченному ключу или None в случае ошибки
    """
    if not output_file:
        output_file = os.path.join("Z:/Keys", "extracted_private_key.asc")
    
    print("🔓 ИЗВЛЕЧЕНИЕ ПРИВАТНОГО КЛЮЧА")
    print("=" * 50)
    
    # Запрос пароля для расшифровки
    password = getpass.getpass("🔑 Введите пароль для расшифровки бэкапа: ")
    
    try:
        # Используем GnuPG для расшифровки
        command = [
            'gpg',
            '--batch',
            '--pinentry-mode', 'loopback',
            '--passphrase', password,
            '--decrypt',
            '--output', output_file,
            backup_file
        ]
        
        print(f"🔄 Расшифровка файла: {backup_file}")
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Ключ успешно извлечен: {output_file}")
            
            # Проверяем содержимое извлеченного файла
            with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'BEGIN PGP PRIVATE KEY BLOCK' in content:
                    print("✅ Обнаружен PGP PRIVATE KEY BLOCK")
                else:
                    print("⚠️  Внимание: файл не содержит стандартный PGP приватный ключ")
            
            return output_file
        else:
            print(f"❌ Ошибка расшифровки: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при извлечении ключа: {e}")
        return None

def import_key_to_keychain(key_file):
    """
    Импортирует извлеченный ключ в GPG keychain
    """
    try:
        command = ['gpg', '--import', key_file]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ключ успешно импортирован в GPG keychain")
            print(result.stdout)
            return True
        else:
            print(f"❌ Ошибка импорта: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при импорте ключа: {e}")
        return False

def list_imported_keys():
    """Показывает список импортированных ключей"""
    try:
        # Список приватных ключей
        print("\n🔑 ИМПОРТИРОВАННЫЕ ПРИВАТНЫЕ КЛЮЧИ:")
        command_private = ['gpg', '--list-secret-keys']
        result_private = subprocess.run(command_private, capture_output=True, text=True)
        print(result_private.stdout)
        
        # Список публичных ключей
        print("🔑 ИМПОРТИРОВАННЫЕ ПУБЛИЧНЫЕ КЛЮЧИ:")
        command_public = ['gpg', '--list-keys']
        result_public = subprocess.run(command_public, capture_output=True, text=True)
        print(result_public.stdout)
        
    except Exception as e:
        print(f"❌ Ошибка при получении списка ключей: {e}")

# 🚀 ОСНОВНАЯ ФУНКЦИЯ
def main():
    """Основной процесс извлечения и импорта ключа"""
    print("=" * 60)
    print("🔄 ПРОЦЕСС ИЗВЛЕЧЕНИЯ КЛЮЧА ИЗ OPENKEYCHAIN BACKUP")
    print("=" * 60)
    
    # 1. Получаем файл бэкапа
    backup_file = get_key_file()
    if not backup_file:
        return
    
    # 2. Извлекаем приватный ключ
    extracted_key = extract_private_key(backup_file)
    if not extracted_key:
        return
    
    # 3. Импортируем ключ в keychain
    print("\n" + "=" * 50)
    print("📥 ИМПОРТ КЛЮЧА В KEYCHAIN")
    print("=" * 50)
    
    import_success = import_key_to_keychain(extracted_key)
    
    if import_success:
        # 4. Показываем импортированные ключи
        list_imported_keys()
        
        # 5. Очистка (опционально) - удаляем временный файл с ключом
        cleanup = input("\n🧹 Удалить временный файл с ключом? (y/N): ")
        if cleanup.lower() == 'y':
            os.remove(extracted_key)
            print("✅ Временный файл удален")
    
    print("\n🎯 ПРОЦЕСС ЗАВЕРШЕН")

if __name__ == "__main__":
    main()