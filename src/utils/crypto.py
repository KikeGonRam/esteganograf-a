from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

def _get_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_message(message: str, password: str, algorithm: str = 'Fernet') -> str:
    if algorithm == 'Fernet':
        key = _get_key(password)
        f = Fernet(key)
        token = f.encrypt(message.encode())
        return token.decode()
    elif algorithm == 'AES':
        key = hashlib.sha256(password.encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode()
    else:
        raise ValueError('Algoritmo no soportado')

def decrypt_message(token: str, password: str, algorithm: str = 'Fernet') -> str:
    if algorithm == 'Fernet':
        key = _get_key(password)
        f = Fernet(key)
        return f.decrypt(token.encode()).decode()
    elif algorithm == 'AES':
        key = hashlib.sha256(password.encode()).digest()
        raw = base64.b64decode(token)
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    else:
        raise ValueError('Algoritmo no soportado')
