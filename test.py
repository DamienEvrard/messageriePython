from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# permet de chiffrer un message grâce à la clé publique du récepteur
def chiffrerAsym(message) :

    #chiffrement avec la clé publique du récepteur
    with open("public_key_bob.pem", "rb") as f:
        public_key_recepteur = RSA.import_key(f.read())

    # On crée l'encrypteur à partir de la clé publique
    cipher_message = PKCS1_OAEP.new(public_key_recepteur)

    # On chiffre le message avec la clé publique
    ciphertext_message = cipher_message.encrypt(message.encode())

    print(ciphertext_message)

    return ciphertext_message

chiffrerAsym('bonjourtoutlemonde')