from Crypto import Random
from Crypto.PublicKey import RSA

public_key_size = 2048
chunk_size = public_key_size / 8
private_key_location = "/home/pawel/trojan_priv.key"
public_key_location = "/home/pawel/trojan/modules/pbl.key"

def generate_keys():
    random_generator = Random.new().read
    keys = RSA.generate(public_key_size, random_generator)
    with open(private_key_location, "wt") as priv_key_file:
        priv_key_file.write(keys.exportKey())
    with open(public_key_location, "wt") as pbl_key_file:
        pbl_key_file.write(keys.publickey().exportKey())

#run to generate new pair of keys
generate_keys()
