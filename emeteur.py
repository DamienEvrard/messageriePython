#prompt message pour get IP cible
#initialiser communication en asymetrique
#challenger 
#si challenge ok
#envoyer clef symetrique
#communiquer les messages prompt

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import pickle
import socket
import sys


# permet denvoyer un message (string) en le chiffrent avec 
# la clef publique de la machine cible
def envoyerAsym(message):
    messageEncrypted=encryptRSA(message)
    s.sendall(messageEncrypted.encode())


# permet denvoyer un message (string) en le chiffrent avec 
# la clef symetrique obtenue lors de challenge avec la machine cible
def envoyerSym(message):
    messageEncrypted=encryptAES(message)
    s.sendall(messageEncrypted.encode())


# fait attendre la machine jusqu'a reception d'un message chiffré 
# qui sera dechiffré grace a la la clef privée de la machine
def recevoirAsym():
    s.bind((ip, port))
    s.listen(1)
    conn, addr = s.accept()

    message = conn.recv(1024).decode()
    conn.close() 
    messageDecrypted=decryptRSA(message)
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


# challenge la machine cible pour sassurer de son identité 
# et recupere la clef symetrique pour la suite des echanges
def challenge() :
    #génération du challenge
    challenge = input('Saisissez une phrase de challenge : ')
    #chiffrement avec la clé publique du récepteur
    with open("public_key_2.pem", "rb") as f:
        public_key_recepteur = RSA.import_key(f.read())

    # On crée l'encrypteur à partir de la clé publique
    cipher_challenge = PKCS1_OAEP.new(public_key_recepteur)

    # On chiffre le message avec la clé publique
    ciphertext_challenge = cipher_challenge.encrypt(challenge.encode())

    #envoi
    envoyerAsym(ciphertext_challenge,ip)

    #récupération du message déchiffré du récepteur
    message_decrpyte, clef = recevoirAsym().split("|||")

    #comparaison du contenu du message déchiffré au challenge d’origine et validation ou non
    if challenge == message_decrpyte :
        return 1, clef
    else :
        return 0, ""
    
#_______________________________________________________________________________________________________________

ip="0.0.0.0"
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
        message = input("quel est le message à envoyer ? ")
        envoyerSym(message)

    elif choix == "3":
        messageRecu=""
        messageRecu, clefSym=recevoirSym()
        print("le message recu est: "+messageRecu)

    elif choix == "4":
        s.close()
        sys.exit()

