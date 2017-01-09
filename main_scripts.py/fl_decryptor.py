import base64
from Crypto.Cipher import AES
from itertools import islice

key = "XdFcxQRnJIIoLkRW" #integrate with files_lister.py
data_path = "l.data"

def decrypt_word_with_key(data_path):
    result = ""
    global init_vector, cipher
    i = 1
    with open(data_path, "rb") as data:
        for line in data:
            if i == 1:
                init_vector = base64.b64decode(line.strip())
                cipher = AES.new(key, AES.MODE_CBC, init_vector)
                i += 1
            else:
                result += cipher.decrypt(base64.b64decode(line.strip()))
    return result[:len(result)-result.count("`")]

#decryption
print(decrypt_word_with_key(data_path))