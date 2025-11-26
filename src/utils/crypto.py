from cryptography.fernet import Fernet
import base64
import hashlib

def _get_key(password: str) -> bytes:
    # Deriva una clave de 32 bytes a partir de la contraseña
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_message(message: str, password: str) -> str:
    key = _get_key(password)
    f = Fernet(key)
    token = f.encrypt(message.encode())
    return token.decode()

def decrypt_message(token: str, password: str) -> str:
    key = _get_key(password)
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()
