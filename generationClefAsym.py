from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pickle


#creer un couple de clefs (publique et privée) pour pouvoir communiquer avec un chiffrement asymétrique
hash_object = SHA256.new(data=b'First')
print(hash_object.hexdigest())
key = RSA.generate(1024)
hash_object = SHA256.new(data=pickle.dumps(key.publickey().export_key('DER')))

with open ("private_key_1.pem", "w") as prv_file:
    print("{}".format(key.exportKey()), file=prv_file)

with open ("public_key_1.pem", "w") as pub_file:
    print("{}".format(key.publickey().exportKey()), file=pub_file)