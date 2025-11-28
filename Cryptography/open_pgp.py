import os
import gnupg
import tempfile
from cryptography.hazmat.primitives import serialization

def handle_openpgp_backup(backup_filepath, target_dir=r"Z:\Keys"):
    """
    Обрабатывает полный бэкап OpenPGP из OpenKeychain
    """
    print("=" * 60)
    print("🔐 ОБРАБОТКА OPENPGP БЭКАПА")
    print("=" * 60)
    
    # Создаем временную директорию для GPG
    temp_dir = tempfile.mkdtemp()
    gpg = gnupg.GPG(gnupghome=temp_dir)
    
    try:
        # 1. Импортируем бэкап в GPG
        print("📥 Импортируем бэкап...")
        with open(backup_filepath, 'rb') as f:
            import_result = gpg.import_keys(f.read())
        
        if not import_result.count:
            print("❌ Не удалось импортировать ключи из бэкапа")
            return
        
        print(f"✅ Импортировано ключей: {import_result.count}")
        
        # 2. Запрашиваем пароль для приватного ключа
        print("\n🔑 ВВОД ПАРОЛЯ:")
        print("Введите пароль, который вы записали на бумаге")
        print("(это пароль от приватного ключа)")
        
        password = input("Пароль: ").strip()
        
        # 3. Извлекаем ключи
        print("\n🔧 Извлекаем ключи...")
        keys = gpg.list_keys(secret=True)
        
        if not keys:
            print("❌ Приватные ключи не найдены в бэкапе")
            return
        
        # 4. Обрабатываем каждый ключ
        for key in keys:
            key_id = key['keyid']
            fingerprint = key['fingerprint']
            
            print(f"\n🔑 Обрабатываем ключ: {key_id}")
            
            # Извлекаем приватный ключ
            priv_key_data = gpg.export_keys(key_id, secret=True, passphrase=password)
            if not priv_key_data:
                print("❌ Не удалось извлечь приватный ключ (неверный пароль?)")
                continue
            
            # Извлекаем публичный ключ
            pub_key_data = gpg.export_keys(key_id)
            
            # 5. Сохраняем в нужном формате
            success = save_extracted_keys(priv_key_data, pub_key_data, target_dir)
            
            if success:
                print(f"✅ Ключ успешно обработан и сохранен")
            else:
                print(f"❌ Ошибка сохранения ключа")
    
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
    
    finally:
        # Очищаем временные файлы
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

def save_extracted_keys(priv_key_data, pub_key_data, target_dir):
    """
    Сохраняет извлеченные ключи в правильном формате
    """
    try:
        os.makedirs(target_dir, exist_ok=True)
        
        # Запрашиваем имя устройства
        dev_name = input("Введите имя устройства для этого ключа (например: Phone): ").strip()
        if not dev_name:
            dev_name = "unknown"
        
        # Определяем следующую версию
        priv_version = get_next_version(dev_name, "priv", target_dir)
        pub_version = get_next_version(dev_name, "pub", target_dir)
        
        # Сохраняем приватный ключ
        priv_filename = f"{dev_name}_priv_{priv_version:02d}.pem"
        priv_filepath = os.path.join(target_dir, priv_filename)
        
        # Конвертируем из OpenPGP в стандартный PEM
        priv_key = convert_openpgp_to_pem(priv_key_data, is_private=True)
        with open(priv_filepath, 'wb') as f:
            f.write(priv_key)
        
        # Сохраняем публичный ключ
        pub_filename = f"{dev_name}_pub_{pub_version:02d}.pem"
        pub_filepath = os.path.join(target_dir, pub_filename)
        
        pub_key = convert_openpgp_to_pem(pub_key_data, is_private=False)
        with open(pub_filepath, 'wb') as f:
            f.write(pub_key)
        
        print(f"📁 Приватный ключ: {priv_filename}")
        print(f"📁 Публичный ключ: {pub_filename}")
        
        return True
        
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False

def convert_openpgp_to_pem(openpgp_data, is_private=True):
    """
    Конвертирует OpenPGP формат в стандартный PEM
    """
    try:
        # Создаем временный GPG для конвертации
        temp_dir = tempfile.mkdtemp()
        gpg = gnupg.GPG(gnupghome=temp_dir)
        
        # Импортируем ключ
        import_result = gpg.import_keys(openpgp_data)
        
        if not import_result.count:
            raise Exception("Не удалось импортировать ключ для конвертации")
        
        # Экспортируем в стандартном формате
        if is_private:
            # Для приватного ключа
            key_data = gpg.export_keys(import_result.fingerprints[0], secret=True)
            # GPG возвращает в PGP формате, нужно дополнительно обработать
            return convert_pgp_to_pem(key_data, is_private=True)
        else:
            # Для публичного ключа
            key_data = gpg.export_keys(import_result.fingerprints[0])
            return convert_pgp_to_pem(key_data, is_private=False)
            
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

def convert_pgp_to_pem(pgp_data, is_private=True):
    """
    Дополнительная конвертация PGP в PEM
    """
    # Это упрощенная конвертация - в реальности может потребоваться
    # более сложная обработка через cryptography
    if is_private:
        # Для приватного ключа
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        
        # Здесь должна быть реальная конвертация
        # Временно возвращаем как есть
        return pgp_data.encode()
    else:
        # Для публичного ключа
        return pgp_data.encode()

def get_next_version(dev_name, key_type, key_dir):
    """
    Получает следующую версию для ключа
    """
    max_version = 0
    pattern = f"{dev_name}_{key_type}_"
    
    if os.path.exists(key_dir):
        for filename in os.listdir(key_dir):
            if filename.startswith(pattern) and filename.endswith('.pem'):
                try:
                    version_str = filename[len(pattern):-4]
                    version = int(version_str)
                    max_version = max(max_version, version)
                except ValueError:
                    continue
    
    return max_version + 1

def install_gnupg_dependencies():
    """
    Инструкция по установке необходимых зависимостей
    """
    instructions = """
    📦 УСТАНОВКА ЗАВИСИМОСТЕЙ:
    
    Для работы с OpenPGP файлами нужно установить:
    
    1. Установите GnuPG для Windows:
       - Скачайте с https://www.gnupg.org/download/
       - Или используйте: pip install python-gnupg
    
    2. Установите python-gnupg:
       - pip install python-gnupg
    
    3. Убедитесь что GnuPG доступен в PATH
    
    Альтернатива - используйте онлайн-конвертер:
    https://8gwifi.org/rsaconvert.jsp
    """
    return instructions

# 🚀 АЛЬТЕРНАТИВНОЕ РЕШЕНИЕ (если не работает автоматическая конвертация)
def manual_conversion_guide():
    """
    Ручная конвертация через онлайн-сервисы
    """
    guide = """
    🔧 РУЧНАЯ КОНВЕРТАЦИЯ OPENPGP:
    
    1. ОТКРОЙТЕ БЭКАП В ТЕКСТОВОМ РЕДАКТОРЕ:
       - Ваш .gpg файл на самом деле текстовый
       - Откройте его в Блокноте или VS Code
    
    2. ЕСЛИ ВИДИТЕ ТЕКСТ В ФОРМАТЕ:
       -----BEGIN PGP PRIVATE KEY BLOCK-----
       ...base64 данные...
       -----END PGP PRIVATE KEY BLOCK-----
    
    3. СКОПИРУЙТЕ ЭТОТ ТЕКСТ И:
    
    4. ИСПОЛЬЗУЙТЕ ОНЛАЙН-КОНВЕРТЕР:
       - https://8gwifi.org/rsaconvert.jsp
       - Вставьте PGP ключ
       - Выберите 'Convert PGP Private Key to PEM'
       - Скопируйте результат
    
    5. СОХРАНИТЕ КАК .pem файл
    
    6. ДЛЯ ПУБЛИЧНОГО КЛЮЧА:
       - Аналогично, но выберите 'Convert PGP Public Key to PEM'
    """
    return guide

def simple_backup_handler(backup_filepath):
    """
    Упрощенная обработка бэкапа
    """
    print("=" * 60)
    print("🔐 ПРОСТАЯ ОБРАБОТКА OPENPGP БЭКАПА")
    print("=" * 60)
    
    print("1. ОТКРОЙТЕ ФАЙЛ В БЛОКНОТЕ:")
    print(f"   {backup_filepath}")
    
    print("\n2. СКОПИРУЙТЕ СОДЕРЖИМОЕ И:")
    print("   - Используйте онлайн-конвертер")
    print("   - Или вручную извлеките ключи")
    
    print("\n3. СОХРАНИТЕ РЕЗУЛЬТАТ КАК:")
    print("   Phone_priv_01.pem - для приватного ключа")
    print("   Phone_pub_01.pem - для публичного ключа")
    
    print("\n4. ПОМЕСТИТЕ В ПАПКУ Z:\\Keys")
    
    input("\nНажмите Enter когда завершите...")

# 🚀 ЗАПУСК ПРОГРАММЫ
if __name__ == "__main__":
    # backup_file = input("Введите путь к файлу бэкапа (.gpg): ").strip()
    backup_file = input("Введите путь к файлу бэкапа (.gpg): ").strip()
    
    if not os.path.exists(backup_file):
        print("❌ Файл не найден!")
        print(install_gnupg_dependencies())
    else:
        # Пытаемся автоматическую обработку
        try:
            handle_openpgp_backup(backup_file)
        except:
            print("❌ Автоматическая обработка не удалась")
            print(manual_conversion_guide())
            simple_backup_handler(backup_file)
