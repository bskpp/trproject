import base64

from Crypto.PublicKey import RSA
import ast

pub_key_size = 16 #integrate with files_stealer.py
private_key_path = "/home/pawel/trojan_priv.key"
content_data_path = "s.data"


def get_private_key():
    with open(private_key_path, "rt") as priv_key:
        return RSA.importKey(priv_key.read())


def decrypt_file_content_with_private_key(data_path):
    result = ""
    priv_key = get_private_key()
    with open(data_path, "rb") as data:
        for line in data:
            result += priv_key.decrypt(base64.b64decode(line.strip()))
    return result

#decryption
print(decrypt_file_content_with_private_key(content_data_path))