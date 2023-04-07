import socket

# Création de la socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adresse IP et port du serveur
ip = '192.168.43.217'
port = 1234

# Lier la socket à l'adresse IP et au port spécifiés
s.bind((ip, port))

# Nombre maximal de connexions en attente
s.listen(1)
print(f"Serveur en attente de connexion sur {ip}:{port}")

# Accepter la connexion
conn, addr = s.accept()
print(f"Connexion établie avec {addr[0]}:{addr[1]}")

# Recevoir les données
data = conn.recv(1024).decode()
print(f"Message reçu : {data}")

# Fermer la connexion
conn.close()