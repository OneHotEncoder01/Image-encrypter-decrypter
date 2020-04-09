#! /home/masteruser/anaconda3/bin/python3

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from PIL import Image



filename = input("Enter the name of the File : ")
image = Image.open(filename)

width, height = image.size
print('image width = ',width)
print("\n")
print('image height = ',height)
print("\n")
layout = []



for x in range(width):
    for y in range(height):
        layout.append(image.getpixel((x, y)))


password_provided = "password"
password = password_provided.encode()
salt = b':8\xd4\xaas\x1bm\xdb\xb1\x91\x1e\xc5@\x84\x0bm'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))

crypt_layout = ''.join(str(e) for e in layout)
byte_layout = crypt_layout.encode('utf-8')

f = Fernet(key)
encrypted = f.encrypt(byte_layout)
encrypted_image = encrypted.decode('utf-8')

file1 = open("new_file.txt","w")
file1.write(encrypted_image)
file1.close()

print("new_file.txt has been created ")


