from PIL import Image
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import re

password_provided = "password" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b':8\xd4\xaas\x1bm\xdb\xb1\x91\x1e\xc5@\x84\x0bm' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once



Filename = input("Enter the filename : ")
width = int(input("Enter the width : "))
height = int(input("Enter the height : "))
num_pixel = width*height
f = open(Filename, "r")
encrypted = f.read()
f = Fernet(key)

crypt_layout = ''.join(str(e) for e in encrypted)
byte_layout = crypt_layout.encode('utf-8')

decrypted = f.decrypt(byte_layout)

none_byte = decrypted.decode()
str_layout = re.findall(r'\d+',none_byte)


image = Image.new('RGBA',(width + 1, height + 1))
nn = 0
n = 0
s = 0   
final = [ ]
for i in range(num_pixel):
    s+=3
    final.append(str_layout[(s-3):s])

lst = list(final)
print(type(lst))
print(final[0])
for x in range(int(width)):
    for y in range(height):
        son = lst[nn]
        image.putpixel((x, y), (int(son[n]), int(son[n+1]), int(son[n+2]), 255))
        nn = nn + 1
image.show()

