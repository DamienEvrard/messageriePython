import socket
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP

# Création de la socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Adresse IP et port du serveur
# ip = '192.168.43.217'
# port = 1234

# # Lier la socket à l'adresse IP et au port spécifiés
# s.bind((ip, port))

# # Nombre maximal de connexions en attente
# s.listen(1)
# print(f"Serveur en attente de connexion sur {ip}:{port}")

# # Accepter la connexion
# conn, addr = s.accept()
# print(f"Connexion établie avec {addr[0]}:{addr[1]}")

# # Recevoir les données
# data = conn.recv(1024).decode()
# print(f"Message reçu : {data}")

# # Fermer la connexion
# conn.close()

serveur_adress = ('', 1234)
s.bind(serveur_adress)

data, addressEnvoi = s.recvfrom(4096)

# On récupère la clé privée depuis le fichier
with open("private_key_bob.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

# On crée le décrypteur à partir de la clé privée
cipher = PKCS1_OAEP.new(private_key)

# On décrypte le message avec la clé privée
message = cipher.decrypt(data) 
print(message)