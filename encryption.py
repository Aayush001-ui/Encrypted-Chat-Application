from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from utils.config import ENCRYPTION_KEY

def get_cipher():
    key = urlsafe_b64encode(ENCRYPTION_KEY.ljust(32, b'\0'))
    return Fernet(key)

def encrypt_message(message):
    cipher = get_cipher()
    return cipher.encrypt(message.encode())

def decrypt_message(ciphertext):
    cipher = get_cipher()
    return cipher.decrypt(ciphertext).decode()
