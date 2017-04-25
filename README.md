
# Station Meteo IoT
TODO: Créer une station météo en utilisant des Raspberry Pi
## Installation
TODO: Télécharger simplement ou clonez le projet git
## Usage
TODO: 
1. Télécharger le projet
2. Lancer le script Python ( python mainFlask.py ) sur la Raspberry qui servira d'afficheur
3. Lancer le script Python ( python meteo.py) sur la Raspberry qui enverra les données
4. Installer Jeedom sur la 3eme Raspberry
5. Pour utiliser le site web, télécharger le dossier subscriber et exécuter ( node app.js ) le serveur Node
6. Récupérer les url des Requetes pour les scripts de scénario
7. C'est parti !

## Swagger

#### Python Flask

https://app.swaggerhub.com/apis/MrSqueezeR/Flask_Meteo/1.0.0 

#### MQTT

Swagger ne prend pas en compte MQTT, il est normal donc que dans le Scheme on ait https

https://app.swaggerhub.com/apis/jpetitfils/meteoStation/1.0.0