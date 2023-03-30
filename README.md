# messageriePython

Ces programmes permetent d'envoyer et de recevoir des messages entre 2 machines d'un LAN, en utilisant le chiffrement hybride.

## A faire avant lacement du programme:
Executer le programme de generation des clefs asymetrique sur les 2 machines.
Echanger les clefs publique entre les 2 machines pour simuler la reception de ces clef depuis un serveur de stockage de confiance.

### Lancer le programme emeteur.py sur la machine
- Grace au menu naviguer jusqu'a la saisi de l'ip de la machine cible.
- Le programme va challenger la machine cible afin de l'autentifier.
- Si la machine est bien autentifié, elle transmetra alors une clef symetrique dans sa reponse pour que le chiffrement se fasse 
de facon symetrique pour la suite des echanges.
- Naviguer via le menu dans l'envoie de mesage et suivre les indications du programme.
- Vous pouvez passer en mode reception pour recevoir a votre tour un message.


### Lancer le programme recepteur.py sur la machine cible
- Tant que la machine ne recoit pas de connexion entrant elle ne permet pas d'envoyer de message.
- Lors que la premiere connexion est detectee (correspondant au challenge), le programme va dechiffrer le message a l'aide de sa clef privee 
puis va generer une clef symetrique et envoyer en chiffant avec la clef publique de la machine emettrice le la clef symetrique concatenee au challenge.
- Vous pouvez desormer naviguer dans le menu pour envoyer ou recevoir un message.
