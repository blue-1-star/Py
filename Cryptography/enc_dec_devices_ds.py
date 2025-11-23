import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

save_dir = r"Z:\Keys"
password = b'my_secure_password'  # пароль для приватных ключей

# Вспомогательная функция для получения максимального номера существующих ключей
def get_max_key_version(dev_name, key_type):
    max_version = 0
    prefix = f"{dev_name}_{key_type}_"
    
    for filename in os.listdir(save_dir):
        if filename.startswith(prefix) and filename.endswith('.pem'):
            try:
                # Извлекаем номер из формата {dev_name}_{key_type}_{nn}.pem
                version_str = filename[len(prefix):-4]  # убираем .pem
                version = int(version_str)
                max_version = max(max_version, version)
            except ValueError:
                continue
    return max_version

# Функция для загрузки существующих ключей
def load_existing_keys(dev_name, key_type, version):
    filename = os.path.join(save_dir, f"{dev_name}_{key_type}_{version:02d}.pem")
    
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, "rb") as f:
            key_data = f.read()
        
        if key_type == "priv":
            return serialization.load_pem_private_key(key_data, password=password)
        else:
            return serialization.load_pem_public_key(key_data)
    
    except Exception as e:
        print(f"Ошибка загрузки ключа {filename}: {e}")
        return None

# Функция для сохранения ключей
def save_key(key, dev_name, key_type, version):
    filename = os.path.join(save_dir, f"{dev_name}_{key_type}_{version:02d}.pem")
    
    try:
        if key_type == "priv":
            key_bytes = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password)
            )
        else:
            key_bytes = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        
        with open(filename, "wb") as f:
            f.write(key_bytes)
        
        print(f"Ключ сохранен: {filename}")
        return True
    
    except Exception as e:
        print(f"Ошибка сохранения ключа {filename}: {e}")
        return False

# Основная функция для работы с ключами устройства
def manage_device_keys(dev_name, force_create=False):
    # Проверяем существующие версии ключей
    max_priv_version = get_max_key_version(dev_name, "priv")
    max_pub_version = get_max_key_version(dev_name, "pub")
    
    # Если ключи уже существуют и не требуется принудительное создание
    if max_priv_version > 0 and max_pub_version > 0 and not force_create:
        print(f"{dev_name.upper()}: Ключи уже существуют (версия {max_priv_version:02d})")
        
        # Загружаем существующие ключи
        priv_key = load_existing_keys(dev_name, "priv", max_priv_version)
        pub_key = load_existing_keys(dev_name, "pub", max_pub_version)
        
        if priv_key and pub_key:
            return priv_key, pub_key, max_priv_version
    
    # Создаем новые ключи
    print(f"{dev_name.upper()}: Создание новых ключей...")
    
    # Определяем следующую версию
    next_version = max(max_priv_version, max_pub_version) + 1
    
    # Генерируем новую пару ключей
    priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub_key = priv_key.public_key()
    
    # Сохраняем ключи
    if save_key(priv_key, dev_name, "priv", next_version) and \
       save_key(pub_key, dev_name, "pub", next_version):
        print(f"{dev_name.upper()}: Ключи созданы (версия {next_version:02d})")
        return priv_key, pub_key, next_version
    else:
        raise Exception(f"Не удалось создать ключи для устройства {dev_name}")

# Функция для загрузки ключей с других устройств
def load_keys_from_device(dev_name, version=None):
    if version is None:
        # Ищем максимальную версию
        version = get_max_key_version(dev_name, "priv")
        if version == 0:
            version = get_max_key_version(dev_name, "pub")
    
    if version == 0:
        raise Exception(f"Ключи для устройства {dev_name} не найдены")
    
    print(f"Загрузка ключей устройства {dev_name} (версия {version:02d})...")
    
    priv_key = load_existing_keys(dev_name, "priv", version)
    pub_key = load_existing_keys(dev_name, "pub", version)
    
    if priv_key and pub_key:
        return priv_key, pub_key
    else:
        raise Exception(f"Не удалось загрузить ключи для устройства {dev_name}")

# Функции шифрования/дешифрования
def encrypt_message(message, pub_key):
    encrypted = pub_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_message(encrypted_message, priv_key):
    decrypted = priv_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

# Пример использования
if __name__ == "__main__":
    # Создаем директорию если не существует
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        # 1. Управление ключами для локальных устройств
        print("=== ЛОКАЛЬНЫЕ УСТРОЙСТВА ===")
        priv_A, pub_A, version_A = manage_device_keys("A")
        priv_B, pub_B, version_B = manage_device_keys("B")
        
        # 2. Загрузка ключей с других устройств (имитация)
        print("\n=== ВНЕШНИЕ УСТРОЙСТВА ===")
        # Предположим, что у нас есть ключи от смартфона и планшета
        try:
            priv_phone, pub_phone = load_keys_from_device("Phone", 1)
            print("Ключи смартфона загружены")
        except Exception as e:
            print(f"Смартфон: {e}")
        
        try:
            priv_tablet, pub_tablet = load_keys_from_device("Tablet", 1)
            print("Ключи планшета загружены")
        except Exception as e:
            print(f"Планшет: {e}")
        
        # 3. Демонстрация работы
        print("\n=== ДЕМОНСТРАЦИЯ РАБОТЫ ===")
        
        # Сообщение от A к B
        message = "Сообщение от A к B"
        encrypted = encrypt_message(message, pub_B)
        decrypted = decrypt_message(encrypted, priv_B)
        print(f"Шифрование A->B: {decrypted}")
        
        # Сообщение от B к A
        message = "Сообщение от B к A"
        encrypted = encrypt_message(message, pub_A)
        decrypted = decrypt_message(encrypted, priv_A)
        print(f"Шифрование B->A: {decrypted}")
        
        # Если бы были ключи от других устройств:
        # encrypted = encrypt_message("Сообщение для смартфона", pub_phone)
        # Можно сохранить и отправить на смартфон для дешифровки
        
    except Exception as e:
        print(f"Ошибка: {e}")
