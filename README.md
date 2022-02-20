# oc_p12_epicevents
Projet réalisé dans le cadre de ma formation OpenClassrooms Développeur d'Applications Python.  
Il s'agit d'une API réalisée avec Django pour une société fictive d'évenementiel, EpicEvents.  
L'application permet de gérer des clients, contrats et événements via une API REST et une interface d'administration.

## Features

Tout les endpoints, leurs détails ainsi que des exemples d'utilisation sont décrits dans la [documentation](https://documenter.getpostman.com/view/18605508/UVkjuwoN). 

## Installation & lancement

Commencez tout d'abord par installer Python.  
Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/FlorianMgs/oc_p12_epicevents.git
```
Placez vous dans le dossier oc_p12_epicevents, puis créez un nouvel environnement virtuel:
```
python -m venv env
```
Ensuite, activez-le.
Windows:
```
env\scripts\activate.bat
```
Linux:
```
source env/bin/activate
```
Installez ensuite les packages requis:
```
pip install -r requirements.txt
```
Ensuite, placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations:
```
python manage.py makemigrations
```
Puis: 
```
python manage.py migrate
```
Il ne vous reste plus qu'à lancer le serveur: 
```
python manage.py runserver
```
Vous pouvez ensuite utiliser l'applicaton via les différents endpoints décrits dans la documentation. 
Pour accéder aux fonctionnalités de l'application en tant qu'administrateur, utilisez les identifiants suivant:
- management@epicevents.io
- passtest   
sur ce endpoint: http://127.0.0.1:8000/api/login/ ou à cette addresse: http://127.0.0.1:8000/admin
