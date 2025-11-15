import os

# Настройки
save_dir = r"Z:\Keys"
base_name_privat = "nuc_py_privat_"
base_name_pub = "nuc_py_pub_"
file_extension = "" # можно добавить расширение, например .pem, .p12

# Создаем папку если нет
os.makedirs(save_dir, exist_ok=True)

# Находим уже существующие номера файлов
def get_next_filename(base_name):
    i = 1
    while True:
        filename = os.path.join(save_dir, f"{base_name}{i:02d}{file_extension}")
        if not os.path.exists(filename):
            return filename
        i += 1

# Определяем имена файлов
priv_filename = get_next_filename(base_name_privat)
pub_filename = get_next_filename(base_name_pub)

# Пароль для приватных ключей (замените по необходимости)
password = b'te_24!@ljg'

# 1. Генерация пар ключей
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

# 2. Сохраняем приватный ключ (зашифрованный паролем)
pem_priv = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(password),
)
with open(priv_filename, "wb") as f:
    f.write(pem_priv)
print(f"Приватный ключ сохранен: {priv_filename}")

# 3. Сохраняем публичный ключ
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
with open(pub_filename, "wb") as f:
    f.write(public_bytes)
print(f"Публичный ключ сохранен: {pub_filename}")

# --- Теперь загрузка ключей из файлов для теста ---

# Загрузка приватного ключа
with open(priv_filename, "rb") as f:
    priv_data = f.read()
private_key_loaded = serialization.load_pem_private_key(
    priv_data,
    password=password,
)

# Загрузка публичного ключа (подразумевается, что есть публичный ключ второго участника)
# В этом примере для теста используем свой публичный
with open(pub_filename, "rb") as f:
    pub_data = f.read()
public_key_loaded = serialization.load_pem_public_key(pub_data)

# 4. Шифрование сообщения публичным ключом другого участника
message = "Это секретное сообщение".encode('utf-8')

ciphertext = public_key_loaded.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Сообщение зашифровано.")

# 5. Расшифровка своим приватным ключом
decrypted_message = private_key_loaded.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Расшифровано:", decrypted_message.decode())
