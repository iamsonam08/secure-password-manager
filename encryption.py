from cryptography.fernet import Fernet
import os

def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()

    return key


def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())


def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()