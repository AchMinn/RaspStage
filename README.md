# RaspStage
le stage consiste d'un déploiement d’un dôme aménagé type studio équipé d’objets connectés (IoT) et d’intelligence artificielle (IA). le dôme sera doté de plusieurs systèmes qui permettent le control et le maintien du confort de l’occupant dans le bâtiment à travers le monitoring en temps réels et le control des objets connectés.
Il s’agit principalement de :
    • Décrire l'architecture générale du réseau, y compris les composants principaux (routeurs, commutateurs, point d'accès Wi-Fi) et effectuer les configurations réseau des dispositifs IoT et des différents composants du système.
    • Définir les configurations logicielles du Raspberry pour accomplir ces fonctions et spécifier les algorithmes et les processus de traitement des données qui seront exécutés localement sur les Raspberry Pi.
    • Déploiement de l’application web sur un serveur local
    • Mettre à jour l’interface utilisateur pour intégrer les nouvelles fonctionnalités 
    • Intégration avec l'IA : Implémenter des systèmes intelligents telles que la reconnaissance faciale, la commande vocale ou des systèmes de prédictions ou de recommandations générées par l’IA ;

# Things needed for a proper set up 

- Raspios installed on sd card
- screen, keyboard, mouse to get wifi, then do it remotely
- Fixed ip so remote control doesn't get pegged ( In case it does, use nmap to get the ip )

- Install an IDE if you want to edit using the rasp - Security settings config ( Turn on SSH, SPI, I2C...)
  
# development experience usually goes like :

- Develop in your IDE
- Publish to a directory 
	- Deployment to be self contained
	- Target runtime "linux-arm"
	- Target framework "net5.0"
   For targets change up the yml 
- SFTP files to the raspberry pi using FileZilla "https://thirtythreedown.github.io/SOFTPiEasySFTPFileTransfer.html"
- VNC (Setting up permissions to run your code)
	- chown <user> <Directory or File> e.g chown pi ./Control
	- chmod +777 <Directory or File> e.g chmod +777 ./Control
	- ./<Dll Name> e.g ./Control
