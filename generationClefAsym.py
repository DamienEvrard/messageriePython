from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pickle




print("1: emeteur")
print("2: recepteur")
nom=input("quel est le role de cette machine?")



#creer un couple de clefs (publique et privée) pour pouvoir communiquer avec un chiffrement asymétrique
hash_object = SHA256.new(data=b'First')
print(hash_object.hexdigest())
key = RSA.generate(1024)
hash_object = SHA256.new(data=pickle.dumps(key.publickey().export_key('DER')))

with open ("private_key_"+nom+".pem", "w") as prv_file:
    print("{}".format(key.exportKey()), file=prv_file)

with open ("public_key_"+nom+".pem", "w") as pub_file:
    print("{}".format(key.publickey().exportKey()), file=pub_file)