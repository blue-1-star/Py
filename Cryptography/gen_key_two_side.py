import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

save_dir = r"Z:\Keys"
base_name_privat = "nuc_py_privat_"
base_name_pub = "nuc_py_pub_"
password = b'my_secure_password'  # пароль для приватных ключей

# Вспомогательная функция для получения следующего свободного номера файла
def get_next_filename(base_name):
    i = 1
    while True:
        filename = os.path.join(save_dir, f"{base_name}{i:02d}")
        if not os.path.exists(filename):
            return filename
        i += 1

# Загружаем или создаем пару ключей для стороны
def load_or_create_keys(side_label):
    priv_files = [f for f in os.listdir(save_dir) if f.startswith(f"{side_label}_priv")]
    pub_files = [f for f in os.listdir(save_dir) if f.startswith(f"{side_label}_pub")]

    if priv_files and pub_files:
        priv_filename = os.path.join(save_dir, sorted(priv_files)[-1])
        pub_filename = os.path.join(save_dir, sorted(pub_files)[-1])

        with open(priv_filename, "rb") as f:
            priv_data = f.read()
        priv_key = serialization.load_pem_private_key(priv_data, password=password)

        with open(pub_filename, "rb") as f:
            pub_data = f.read()
        pub_key = serialization.load_pem_public_key(pub_data)

        print(f"{side_label.upper()}: Ключи загружены из")
        print(priv_filename)
        print(pub_filename)
    else:
        # Генерируем
        priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pub_key = priv_key.public_key()

        # Имена файла
        priv_filename = get_next_filename(f"{side_label}_priv")
        pub_filename = get_next_filename(f"{side_label}_pub")
        # Сохраняем приватный
        priv_bytes = priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password)
        )
        with open(priv_filename, "wb") as f:
            f.write(priv_bytes)

        # Сохраняем публичный
        pub_bytes = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(pub_filename, "wb") as f:
            f.write(pub_bytes)

        print(f"{side_label.upper()}: Ключи созданы и сохранены.")
    return priv_key, pub_key

# Загружаем или создаем ключи для обеих сторон
priv_A, pub_A = load_or_create_keys("A")
priv_B, pub_B = load_or_create_keys("B")

# # Теперь тестируем обмен сообщениями:  
message_A_to_B = "Сообщение от A к B".encode('utf-8')
message_B_TO_A = "Сообщение от B к A".encode('utf-8')

# --- A шифрует сообщение для B ---

ciphertext_A_to_B = pub_B.encrypt(
    message_A_to_B,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("A зашифровал сообщение для B.")

# --- B расшифровывает ---  
dec_message_A_B = priv_B.decrypt(
    ciphertext_A_to_B,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("B расшифровал сообщение от A:", dec_message_A_B.decode())

# --- B шифрует сообщение для A ---

ciphertext_B_to_A = pub_A.encrypt(
    message_B_TO_A,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("B зашифровал сообщение для A.")

# --- A расшифровывает ---
dec_message_B_A = priv_A.decrypt(
    ciphertext_B_to_A,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("A расшифровал сообщение от B:", dec_message_B_A.decode())


# 1. Если в каталоге присутствуют ключи A_priv01, B_priv01 последующую версию 02 уже не нужно генерировать
#2. Предусмотреть возможность шифрования- дешифрования на десктопе сообщений с ключами, сгенерированными и работающими на других девайсах ( смартфон, планшет, андроид, ИОС ... ) 
#{Dev-Name}_priv_{nn},  {Dev-Name}_pub_{nn}
#с тем чтобы иметь возможность шифровать/ дешифровать на десктопе сообщения с любых устройств. 