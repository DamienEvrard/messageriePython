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
from Crypto.Random import get_random_bytes

def chiffrerAsym(message) :

    #chiffrement avec la clé publique du récepteur
    with open("public_key_alice.pem", "rb") as f:
        public_key_recepteur = RSA.import_key(f.read())

    # On crée l'encrypteur à partir de la clé publique
    cipher = PKCS1_OAEP.new(public_key_recepteur)

    # On chiffre le message avec la clé publique
    ciphertext = cipher.encrypt(message.encode()) 

    # On chiffre le challenge avec la clé publique
    return ciphertext

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

    serveur_adress = (ip, port)

    message_chiffre = chiffrerAsym(message)
    s.sendto(message_chiffre, serveur_adress)

# permet d'envoyer un message (string) en le chiffrant avec 
# la clé symétrique obtenue lors du challenge avec le récepteur
def envoyerSym(message):
    messageEncrypted=chiffrerSym(message)

    adresse_serveur = (ip, port)
    s.sendto(messageEncrypted, adresse_serveur)


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
    print ("réception Symetrique")
    data = s.recvfrom(1024)
    print(data)
    message = str(data)
    #conn.close() 
    messageDecrypted=dechiffrerSym(message)
    return messageDecrypted


# challenge la machine cible pour s'assurer de son identité 
# et recupere la clef symetrique pour la suite des echanges
def challenge() :

    challengeAlice=recevoirAsym()
    clefSym=generationClefSym()
    #génération du challenge : chaîne de caractère aléatoire de 10 caractères
    letters = string.ascii_lowercase
    challengeBob = ''.join(random.choice(letters) for i in range(10))
    #construction du message
    messageEnvoye=str(challengeAlice) + "|||"+ str(clefSym) + "|||"+ str(challengeBob)

    envoyerAsym(messageEnvoye)


    challenge_recu=recevoirSym()

    #comparaison du contenu du message déchiffré au challenge d’origine et validation ou non
    if challengeBob == challenge_recu :
        return 1
    else :
        return 0
    
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


#genere une clef symetrique de taille 32 bytes
def generationClefSym():
    return get_random_bytes(10)
    
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
    choix=input("Que voulez-vous faire:")
    
    if choix == "1":
        ip=input("saisir l'ip de la machine cible : ")

        resultat= challenge()
        if resultat == 1:
            print("challenge OK")
        else:
            s.close()
            print("challenge non OK")
        

    elif choix == "2":
        if ip=="":
            print("Vous devez dabord saisir une ip cible ! ")
        else:
            message = input("Quel est le message à envoyer ? ")
            envoyerSym(message)

    elif choix == "3":
        if ip=="":
            print("Vous devez dabord saisir une ip cible !")
        else:
            messageRecu=""
            messageRecu, clefSym=recevoirSym()
            print("Le message recu est : "+messageRecu)

    elif choix == "4":
        s.close()
        sys.exit()

