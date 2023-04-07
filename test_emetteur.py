import socket

# Création de la socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adresse IP et port du serveur
ip = '192.168.43.116'
port = 1234

# Connexion à l'adresse IP et au port spécifiés
s.connect((ip, port))

# Envoi des données
message = 'Hello, world!'
s.sendall(message.encode())
print("Message envoyé")

# Fermeture de la socket
s.close()