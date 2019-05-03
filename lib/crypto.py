from hashlib import pbkdf2_hmac
from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes, random
import json
import string

import base64

def get_key(username, master_password):
    return pbkdf2_hmac('sha256', master_password.encode(), username.encode(), 100000, 32)

def get_auth_hash(username, master_password):
    return pbkdf2_hmac('sha256', get_key(username, master_password), master_password.encode(), 1, 32)

def gen_iv():
    return get_random_bytes(16)

def encrypt_vault(vault_str, key):
    data = pad(vault_str)
    iv = gen_iv()
    aes = AES.new(key, AES.MODE_CBC, iv)
    return iv + aes.encrypt(data)

def decrypt_vault(cipher_text, key):
    iv = cipher_text[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(cipher_text[16:])).decode('utf-8')

def pad(s):
        return s + (32 - len(s) % 32) * chr(32 - len(s) % 32)
def unpad(s):
        return s[:-ord(s[len(s)-1:])]

def generate_password(length, options):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols = '!@#$%^&*?'

    password = list()
    for i in range(length):
        password.append(random.choice(lowercase))

    if 'Uppercase' in options:
        num_to_replace = int(length/5) + 1
        for i in range(num_to_replace):
            replace_idx = random.randint(0, length-1)
            password[replace_idx] = random.choice(uppercase)

    if 'Numbers' in options:
        num_to_replace = int(length/5) + 1
        for i in range(num_to_replace):
            replace_idx = random.randint(0, length-1)
            password[replace_idx] = random.choice(numbers)

    if 'Symbols' in options:
        num_to_replace = int(length/6) + 1
        for i in range(num_to_replace):
            replace_idx = random.randint(0, length-1)
            password[replace_idx] = random.choice(symbols)

    return ''.join(password)
