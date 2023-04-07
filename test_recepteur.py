import socket

# Création de la socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion à l'adresse IP et au port spécifiés
ip = '127.0.0.1'
port = 1234
s.connect((ip, port))

# Envoi des données
message = 'Hello, world!'
s.sendall(message.encode())

# Réception des données envoyées par le serveur
data = s.recv(1024)

# Affichage des données reçues
print("Message reçu :", data.decode())

# Fermeture de la socket
s.close()