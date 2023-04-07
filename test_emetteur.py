from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
import pickle

import socket

# Création de la socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # On génère le couple de clé
# key = RSA.generate(1024)


# # On stocke la clé privée dans un fichier
# with open("private_key.pem", "wb") as f:
#     f.write(key.export_key())

# # On stocke la clé publique dans un fichier
# with open("public_key.pem", "wb") as f:
#     f.write(key.publickey().export_key())

adresse_envoi = '10.187.1.206'
serveur_adress = (adresse_envoi, 1234)


# On lit la clé publique depuis le fichier
with open("public_key_bob.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

message = 'To be encrypted'

# On crée l'encrypteur à partir de la clé publique
cipher = PKCS1_OAEP.new(public_key)

# On chiffre le message avec la clé publique
ciphertext = cipher.encrypt(message.encode()) 
print(ciphertext)

s.sendto(ciphertext, serveur_adress)


# on crée le couple de clés --> on stocke dans des fichiers
# on crée le challenge
# on vérifie que le challenge passe
# si c'est bon : génération de la clé symétrique (code 1)
# partage de la clé symétrique
# on peut échanger des messages avec la clé symétrique