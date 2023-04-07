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


def chiffrerAsym(message) :

    #chiffrement avec la clé publique du récepteur
    with open("public_key_alice.pem", "rb") as f:
        public_key_recepteur = RSA.import_key(f.read())

    # On crée l'encrypteur à partir de la clé publique
    cipher_message = PKCS1_OAEP.new(public_key_recepteur)

    # On chiffre le challenge avec la clé publique
    ciphertext_message = cipher_message.encrypt(message.encode())

    return ciphertext_message

def dechiffrerAsym(message) :

    # On récupère la clé privée de l'émetteur depuis le fichier de clé
    with open("private_key_bob.pem", "rb") as f:
        private_key = RSA.import_key(f.read())

    # On crée le décrypteur à partir de la clé privée
    cipher = PKCS1_OAEP.new(private_key)

    # On décrypte le message avec la clé privée
    message_dechiffre = cipher.decrypt(message) 

    return message_dechiffre

# permet d'envoyer un message (string) en le chiffrant avec 
# la clé publique du récepteur
def envoyerAsym(message):
    messageEncrypted=chiffrerAsym(message)
    s.sendall(messageEncrypted.encode())


# permet d'envoyer un message (string) en le chiffrant avec 
# la clé symétrique obtenue lors du challenge avec le récepteur
def envoyerSym(message):
    messageEncrypted=encryptAES(message)
    s.sendall(messageEncrypted.encode())


# fait attendre la machine jusqu'a reception d'un message chiffré en asymétrique
# qui sera dechiffré grace a la la clé privée de l'émetteur
def recevoirAsym():
    s.bind((ip, port))
    s.listen(1)
    conn, addr = s.accept()

    message = conn.recv(1024).decode()
    conn.close() 
    messageDecrypted=dechiffrerAsym(message)
    return messageDecrypted


# fait attendre la machine jusqu'a reception d'un message chiffré qui sera dechiffré 
# grace a la la clef symetrique obtenue lors de challenge avec la machine cible
def recevoirSym():
    s.bind((ip, port))
    s.listen(1)
    conn, addr = s.accept()

    message = conn.recv(1024).decode()
    conn.close() 
    messageDecrypted=decryptAES(message)
    return messageDecrypted


# challenge la machine cible pour s'assurer de son identité 
# et recupere la clef symetrique pour la suite des echanges
def challenge() :

    #génération du challenge : chaîne de caractère aléatoire de 10 caractères
    letters = string.ascii_lowercase
    challenge_envoye = ''.join(random.choice(letters) for i in range(10))

    # envoyerAsym prend en paramètre le challenge en clair, le chiffre et l'envoie
    envoyerAsym(challenge_envoye)

    #récupération du challenge déchiffré du récepteur
    challenge_recu, cle = recevoirAsym().split("|||")

    #comparaison du contenu du message déchiffré au challenge d’origine et validation ou non
    if challenge_envoye == challenge_recu :
        return 1, cle
    else :
        return 0, ""
    
#_______________________________________________________________________________________________________________

ip=""
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clefSym=""

#boucle infinie qui affiche un menu afin de selectionner l'action a effectuer
while 1:
    print("1: saisir l'ip de la machine cible")
    print("2: envoyer un message")
    print("3: recevoir un message")
    print("4: quitter le programme")
    choix=input("que voulez-vous faire:")
    
    if choix == "1":
        ip=input("saisir l'ip de la machine cible")
        s.connect((ip, port))
        resultat, clefSym = challenge()
        if resultat == 1 :
            print("challenge OK")
        else:
            s.close()
            print("challenge non OK") 

    elif choix == "2":
        if ip=="":
            print("vous devez dabord saisir une ip cible")
        else:
            message = input("quel est le message à envoyer ? ")
            envoyerSym(message)

    elif choix == "3":
        if ip=="":
            print("vous devez dabord saisir une ip cible")
        else:
            messageRecu=""
            messageRecu, clefSym=recevoirSym()
            print("le message recu est: "+messageRecu)

    elif choix == "4":
        s.close()
        sys.exit()

