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

# Fermeture de la socket
s.close()