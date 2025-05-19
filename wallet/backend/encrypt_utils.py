from Crypto.Cipher import AES
import base64
import os

def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def encrypt_data(data, key):
    key = key.ljust(32)[:32].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data).encode())
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted, key):
    key = key.ljust(32)[:32].encode()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted.encode()))
    return decrypted.decode().rstrip('\x01-\x10')