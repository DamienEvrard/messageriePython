#prompt message pour get IP cible
#initialiser communication en asymetrique
#challenger 
#si challenge ok
#envoyer clef symetrique
#communiquer les messages prompt

import math
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import pickle
import socket
import sys

# permet de chiffrer un message grâce à la clé publique du récepteur
def chiffrerAsym(message) :

    #chiffrement avec la clé publique 
    with open("public_key_bob.pem", "rb") as f:
        public_key_recepteur = RSA.import_key(f.read())

    # On crée l'encrypteur à partir de la clé publique
    cipher = PKCS1_OAEP.new(public_key_recepteur)

    # On chiffre le message avec la clé publique
    ciphertext = cipher.encrypt(message.encode()) 

    # On chiffre le challenge avec la clé publique
    return ciphertext

# permet de déchiffrer un message grâce à la clé privée de l'émetteur
def dechiffrerAsym(message) :

    with open("private_key_alice.pem", "rb") as f:
        private_key = RSA.import_key(f.read())

    cipher = PKCS1_OAEP.new(private_key)

    message_dechiffre = cipher.decrypt(message)  

    return message_dechiffre

# permet d'envoyer un message (string) en le chiffrant avec 
# la clé publique du récepteur
def envoyerAsym(message):

    serveur_adress = (ip, port)

    message_chiffre = chiffrerAsym(message)
    s.sendto(message_chiffre, serveur_adress)

# permet d'envoyer un message (string) en le chiffrant avec 
# la clé symétrique obtenue lors du challenge avec le récepteur
def envoyerSym(message):
    messageEncrypted=chiffrerSym(message)

    adresse_serveur = (ip, port)
    s.sendto(messageEncrypted, adresse_serveur)
    #s.sendall(messageEncrypted.encode())

# fait attendre la machine jusqu'a reception d'un message chiffré en asymétrique
# qui sera dechiffré grace a la la clé privée de l'émetteur
def recevoirAsym():

    # s.bind((ip, port))
    # s.listen(1)
    # conn, addr = s.accept()

    serveur_adress = ('', port)
    s.bind(serveur_adress)

    message, addressEnvoi = s.recvfrom(4096)
    #conn.close() 
    message_decrypte=dechiffrerAsym(message)

    return message_decrypte

# fait attendre la machine jusqu'a reception d'un message chiffré qui sera dechiffré 
# grace a la la clef symetrique obtenue lors de challenge avec la machine cible
def recevoirSym():

    # s.bind((ip, port))
    # s.listen(1)
    # conn, addr = s.accept()
    print ("réception")
    data = s.recvfrom(1024)
    print(data)
    message = str(data)
    #conn.close() 
    messageDecrypted=dechiffrerSym(message)
    return messageDecrypted

# permet de chiffrer un message grâce à la clé symétrique
def chiffrerSym(message) :

    # On crée l'encrypteur à partir de la clé symétrique
    cipher = AES.new(clefSym.encode('utf-8'), AES.MODE_CFB, 'This is an IV456'.encode('utf-8'))

    # On chiffre le message avec la clé symétrique
    cipher_text = cipher.encrypt(message)

    return cipher_text

# permet de déchiffrer un message grâce à la clé symétrique
def dechiffrerSym(message) :

    # On crée le décrypteur à partir de la clé symétrique
    cipher = AES.new(clefSym.encode('utf-8'), AES.MODE_CFB, 'This is an IV456'.encode('utf-8'))
    
    # On déchiffre le message avec la clé symétrique
    message_dechiffre = cipher.decrypt(message)

    return message_dechiffre
    

# challenge la machine cible pour sassurer de son identité 
# et recupere la clef symetrique pour la suite des echanges
def challenge() :

    #génération du challenge : chaîne de caractère aléatoire de 10 caractères
    letters = string.ascii_lowercase
    challenge_envoye = ''.join(random.choice(letters) for i in range(10))

    # envoyerAsym prend en paramètre le challenge en clair, le chiffre et l'envoie
    envoyerAsym(challenge_envoye)

    #récupération du challenge et de la clé symétrique déchiffrés, du récepteur
    challenge_recu, cle_symetrique, challenge_bob = recevoirAsym().split("|||")

    #comparaison du contenu du message déchiffré au challenge d’origine et validation ou non
    if challenge_envoye == challenge_recu :
        return 1, cle_symetrique, challenge_bob
    else :
        return 0, "", ""
    
#_______________________________________________________________________________________________________________

ip=""
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clefSym=""



#boucle infinie qui affiche un menu afin de selectionner l'action a effectuer
while 1:
    print("1: Saisir l'ip de la machine cible")
    print("2: Envoyer un message")
    print("3: Recevoir un message")
    print("4: Quitter le programme")
    choix=input("Que voulez-vous faire ? :")
    
    if choix == "1":
        ip=input("Saisir l'ip de la machine cible : ")

        resultat, clefSym, challengeBob = challenge()
        if resultat == 1:
            print("Challenge OK")
            envoyerSym(challengeBob)
        else:
            s.close()
            print("Challenge non OK") 

    elif choix == "2":
        if ip=="":
            print("Vous devez dabord saisir une ip cible !")
        else:
            message = input("quel est le message à envoyer ? : ")
            envoyerSym(message)

    elif choix == "3":
        if ip=="":
            print("Vous devez dabord saisir une ip cible !")
        else:
            messageRecu=""
            messageRecu, clefSym=recevoirSym()
            print("le message recu est : "+messageRecu)

    elif choix == "4":
        s.close()
        sys.exit()

