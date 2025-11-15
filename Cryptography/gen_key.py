from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Генерация пары ключей для стороны A
private_key_A = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key_A = private_key_A.public_key()

# Генерация пары ключей для стороны B
private_key_B = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key_B = private_key_B.public_key()

# Экспорт публичных ключей, чтобы обменяться ими (например, передать по сети)
public_bytes_A = public_key_A.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

public_bytes_B = public_key_B.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("Публичный ключ A:\n", public_bytes_A.decode())
print("Публичный ключ B:\n", public_bytes_B.decode())

# После обмена ключами, стороны загружают чужой публичный ключ обратно
from cryptography.hazmat.primitives import serialization

# Загрузка публичных ключей у стороны A
loaded_public_key_B = serialization.load_pem_public_key(public_bytes_B)

# Загрузка публичных ключей у стороны B
loaded_public_key_A = serialization.load_pem_public_key(public_bytes_A)

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Сообщение, которое нужно зашифровать
# message = b"Это секретное сообщение"
message = "Это секретное сообщение".encode('utf-8')


# A шифрует сообщение для B публичным ключом B
ciphertext = loaded_public_key_B.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Зашифрованное сообщение:", ciphertext)

# B расшифровывает сообщение своим приватным ключом
decrypted_message = private_key_B.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Расшифрованное сообщение:", decrypted_message.decode())

# "Z:\Keys"  nuc_py_privat_01, nuc_py_pub_01
