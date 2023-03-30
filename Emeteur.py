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

def genererClefs():
    hash_object = SHA256.new(data=b'First')
    print(hash_object.hexdigest())
    key = RSA.generate(1024)
    hash_object = SHA256.new(data=pickle.dumps(key.publickey().export_key('DER')))

    with open ("private_key_1.pem", "w") as prv_file:
        print("{}".format(key.exportKey()), file=prv_file)

    with open ("public_key_1.pem", "w") as pub_file:
        print("{}".format(key.publickey().exportKey()), file=pub_file)

def envoyer(message, ip):
    messageEncrypted=encrypt(message)
    s.sendall(messageEncrypted.encode())


def recevoir():
    message = receive()
    messageDecrypted=decrypt(message)






ip="0.0.0.0"
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while 1:
    print("1: saisir l'ip de la machine cible")
    print("2: generer les clefs publique et privée")
    print("3: envoyer un message")
    print("4: recevoir un message")
    print("5: quitter")
    choix=input("que voulez-vous faire:")

    if choix == 1:
        ip=input("saisir l'ip de la machine cible")
        s.connect((ip, port))
        if challenge()==1 :
            print("challenge OK")
        else:
            s.close()
            print("challenge non OK") 

    elif choix == 2:
        genererClefs()

    elif choix == 3:
        message = input("quel est le message à envoyer ? ")
        envoyer(message)

    elif choix == 4:
        messageRecu=recevoir()
        print("le message recu est: "+messageRecu)

    elif choix == 5:
        s.close()
        exit()

